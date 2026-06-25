from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.application.dto.dtos import (
    OrderLineItemResponse,
    OrderResponse,
    PaginatedResponse,
    TransitionOrderStatusRequest,
)
from src.application.ports.cart_repository import CartRepository
from src.application.ports.email_port import EmailPort
from src.application.ports.event_bus import EventBus
from src.application.ports.inventory_repository import InventoryRepository
from src.application.ports.order_repository import OrderRepository
from src.application.ports.product_repository import ProductRepository
from src.application.result import Result
from src.domain.entities.models import Order, OrderLineItem
from src.domain.events.events import LowStockAlert, OrderCancelled, OrderPlaced, StockDepleted
from src.domain.value_objects.common import Money, OrderStatus


class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        cart_repo: CartRepository,
        inventory_repo: InventoryRepository,
        product_repo: ProductRepository,
        email_port: EmailPort,
        event_bus: EventBus | None = None,
    ):
        self._order_repo = order_repo
        self._cart_repo = cart_repo
        self._inventory_repo = inventory_repo
        self._product_repo = product_repo
        self._email_port = email_port
        self._event_bus = event_bus

    def execute(self, user_id: uuid.UUID, cart_id: uuid.UUID) -> Result[OrderResponse, str]:
        cart = self._cart_repo.find_by_id(cart_id)
        if cart is None:
            return Result.failure("Cart not found")
        if not cart.items:
            return Result.failure("Cannot create order from empty cart")

        for item in cart.items:
            inv = self._inventory_repo.find_by_product_id(item.product_id)
            if inv is None or inv.available < item.quantity:
                product = self._product_repo.find_by_id(item.product_id)
                name = product.name if product else "Unknown"
                available = inv.available if inv else 0
                return Result.failure(f"Insufficient stock for '{name}': requested {item.quantity}, available {available}")

        for item in cart.items:
            self._inventory_repo.reserve(item.product_id, item.quantity)

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        line_items = []
        for item in cart.items:
            product = self._product_repo.find_by_id(item.product_id)
            line_items.append(
                OrderLineItem(
                    product_id=item.product_id,
                    product_name=product.name if product else "Unknown",
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=item.unit_price * item.quantity,
                )
            )

        total = Money(amount=sum(i.line_total.amount for i in line_items))
        order = Order(
            id=uuid.uuid4(),
            user_id=user_id,
            line_items=line_items,
            status=OrderStatus.PENDING,
            total=total,
            created_at=now,
            updated_at=now,
        )
        created = self._order_repo.create(order)

        self._cart_repo.delete(cart_id)

        self._email_port.send_order_confirmation(
            to_email=str(user_id),
            order_id=str(created.id),
            total=float(total.amount),
        )

        if self._event_bus:
            self._event_bus.publish(
                OrderPlaced(
                    event_id=uuid.uuid4(),
                    occurred_at=now,
                    order_id=created.id,
                    user_id=user_id,
                    total=float(total.amount),
                )
            )
            for item in line_items:
                inv = self._inventory_repo.find_by_product_id(item.product_id)
                if inv and inv.is_low_stock:
                    self._event_bus.publish(
                        LowStockAlert(
                            event_id=uuid.uuid4(),
                            occurred_at=now,
                            product_id=item.product_id,
                            sku=str(item.product_id),
                            available=inv.available,
                            threshold=inv.low_stock_threshold,
                        )
                    )
                if inv and inv.available <= 0:
                    self._event_bus.publish(
                        StockDepleted(
                            event_id=uuid.uuid4(),
                            occurred_at=now,
                            product_id=item.product_id,
                            sku=str(item.product_id),
                            available=inv.available,
                        )
                    )

        return Result.success(self._to_response(created))

    def _to_response(self, order: Order) -> OrderResponse:
        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            line_items=[
                OrderLineItemResponse(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    quantity=i.quantity,
                    unit_price=str(i.unit_price.amount),
                    line_total=str(i.line_total.amount),
                )
                for i in order.line_items
            ],
            status=order.status.value,
            total=str(order.total.amount),
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


class TransitionOrderStatusUseCase:
    def __init__(self, order_repo: OrderRepository, inventory_repo: InventoryRepository, event_bus: EventBus | None = None):
        self._order_repo = order_repo
        self._inventory_repo = inventory_repo
        self._event_bus = event_bus

    def execute(
        self, order_id: uuid.UUID, request: TransitionOrderStatusRequest
    ) -> Result[OrderResponse, str]:
        order = self._order_repo.find_by_id(order_id)
        if order is None:
            return Result.failure("Order not found")

        try:
            target = OrderStatus(request.status)
        except ValueError:
            return Result.failure(f"Invalid status: {request.status}")

        if not order.status.can_transition_to(target):
            return Result.failure(
                f"Cannot transition from '{order.status.value}' to '{target.value}'"
            )

        if target == OrderStatus.CANCELLED:
            for item in order.line_items:
                self._inventory_repo.release(item.product_id, item.quantity)
            if self._event_bus:
                self._event_bus.publish(
                    OrderCancelled(
                        event_id=uuid.uuid4(),
                        occurred_at=datetime.now(timezone.utc).replace(tzinfo=None),
                        order_id=order_id,
                        user_id=order.user_id,
                    )
                )

        updated = self._order_repo.update_status(order_id, target.value)
        return Result.success(
            OrderResponse(
                id=updated.id,
                user_id=updated.user_id,
                line_items=[
                    OrderLineItemResponse(
                        product_id=i.product_id,
                        product_name=i.product_name,
                        quantity=i.quantity,
                        unit_price=str(i.unit_price.amount),
                        line_total=str(i.line_total.amount),
                    )
                    for i in updated.line_items
                ],
                status=updated.status.value,
                total=str(updated.total.amount),
                created_at=updated.created_at,
                updated_at=updated.updated_at,
            )
        )


class ListOrdersUseCase:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def execute(
        self,
        user_id: uuid.UUID | None = None,
        is_admin: bool = False,
        status: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Result[PaginatedResponse, str]:
        if is_admin:
            orders, total = self._order_repo.list_all(status=status, page=page, per_page=per_page)
        elif user_id:
            orders, total = self._order_repo.find_by_user_id(
                user_id, status=status, page=page, per_page=per_page
            )
        else:
            return Result.failure("Authentication required")

        total_pages = max(1, (total + per_page - 1) // per_page)
        return Result.success(
            PaginatedResponse(
                items=[
                    OrderResponse(
                        id=o.id,
                        user_id=o.user_id,
                        line_items=[
                            OrderLineItemResponse(
                                product_id=i.product_id,
                                product_name=i.product_name,
                                quantity=i.quantity,
                                unit_price=str(i.unit_price.amount),
                                line_total=str(i.line_total.amount),
                            )
                            for i in o.line_items
                        ],
                        status=o.status.value,
                        total=str(o.total.amount),
                        created_at=o.created_at,
                        updated_at=o.updated_at,
                    )
                    for o in orders
                ],
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
            )
        )


class GetOrderUseCase:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def execute(self, order_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False) -> Result[OrderResponse, str]:
        order = self._order_repo.find_by_id(order_id)
        if order is None:
            return Result.failure("Order not found")
        if not is_admin and order.user_id != user_id:
            return Result.failure("Order not found")
        return Result.success(
            OrderResponse(
                id=order.id,
                user_id=order.user_id,
                line_items=[
                    OrderLineItemResponse(
                        product_id=i.product_id,
                        product_name=i.product_name,
                        quantity=i.quantity,
                        unit_price=str(i.unit_price.amount),
                        line_total=str(i.line_total.amount),
                    )
                    for i in order.line_items
                ],
                status=order.status.value,
                total=str(order.total.amount),
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
        )
