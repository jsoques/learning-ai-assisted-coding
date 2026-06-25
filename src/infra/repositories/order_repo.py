from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session, selectinload

from src.application.ports.order_repository import OrderRepository
from src.domain.entities.models import Order, OrderLineItem
from src.domain.value_objects.common import Money, OrderStatus
from src.framework.db.models import OrderLineItemModel, OrderModel


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self._session = session

    def _query(self):
        return self._session.query(OrderModel).options(selectinload(OrderModel.line_items))

    def create(self, order: Order) -> Order:
        model = OrderModel(
            id=str(order.id),
            user_id=str(order.user_id),
            status=order.status.value,
            total=float(order.total.amount),
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        self._session.add(model)
        for item in order.line_items:
            self._session.add(
                OrderLineItemModel(
                    order_id=str(order.id),
                    product_id=str(item.product_id),
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=float(item.unit_price.amount),
                    line_total=float(item.line_total.amount),
                )
            )
        self._session.commit()
        return order

    def find_by_id(self, order_id: uuid.UUID) -> Order | None:
        model = self._query().filter(OrderModel.id == str(order_id)).first()
        return self._to_domain(model) if model else None

    def find_by_user_id(
        self, user_id: uuid.UUID, status: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Order], int]:
        q = self._query().filter(OrderModel.user_id == str(user_id))
        if status:
            q = q.filter(OrderModel.status == status)
        q = q.order_by(OrderModel.created_at.desc())
        total = q.count()
        models = q.offset((page - 1) * per_page).limit(per_page).all()
        return [self._to_domain(m) for m in models], total

    def update_status(self, order_id: uuid.UUID, status: str) -> Order:
        model = self._query().filter(OrderModel.id == str(order_id)).first()
        if model:
            model.status = status
            model.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            self._session.commit()
        return self._to_domain(model) if model else None

    def list_all(
        self, status: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Order], int]:
        q = self._query()
        if status:
            q = q.filter(OrderModel.status == status)
        q = q.order_by(OrderModel.created_at.desc())
        total = q.count()
        models = q.offset((page - 1) * per_page).limit(per_page).all()
        return [self._to_domain(m) for m in models], total

    @staticmethod
    def _to_domain(model: OrderModel) -> Order:
        return Order(
            id=uuid.UUID(model.id),
            user_id=uuid.UUID(model.user_id),
            line_items=[
                OrderLineItem(
                    product_id=uuid.UUID(i.product_id),
                    product_name=i.product_name,
                    quantity=i.quantity,
                    unit_price=Money(amount=Decimal(str(i.unit_price))),
                    line_total=Money(amount=Decimal(str(i.line_total))),
                )
                for i in model.line_items
            ],
            status=OrderStatus(model.status),
            total=Money(amount=Decimal(str(model.total))),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
