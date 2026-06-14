from __future__ import annotations

import uuid
from datetime import datetime

from src.application.dto.dtos import AddCartItemRequest, CartItemResponse, CartResponse
from src.application.ports.cart_repository import CartRepository
from src.application.ports.product_repository import ProductRepository
from src.application.result import Result
from src.domain.entities.models import Cart, CartItem
from src.domain.value_objects.common import ProductStatus


class AddToCartUseCase:
    def __init__(self, cart_repo: CartRepository, product_repo: ProductRepository):
        self._cart_repo = cart_repo
        self._product_repo = product_repo

    def execute(
        self, cart_id: uuid.UUID | None, user_id: uuid.UUID | None, session_id: str | None, request: AddCartItemRequest
    ) -> Result[CartResponse, str]:
        product = self._product_repo.find_by_id(request.product_id)
        if product is None or product.status != ProductStatus.ACTIVE:
            return Result.failure("Product not found or inactive")

        if cart_id is None:
            now = datetime.utcnow()
            cart = Cart(
                id=uuid.uuid4(),
                user_id=user_id,
                session_id=session_id,
                items=[],
                created_at=now,
                updated_at=now,
            )
            cart = self._cart_repo.create(cart)
        else:
            existing = self._cart_repo.find_by_id(cart_id)
            if existing is None:
                return Result.failure("Cart not found")
            cart = existing

        existing_item = next((i for i in cart.items if i.product_id == request.product_id), None)
        if existing_item:
            cart.items.remove(existing_item)
        cart.items.append(
            CartItem(
                product_id=request.product_id,
                quantity=request.quantity if existing_item is None else existing_item.quantity + request.quantity,
                unit_price=product.price,
            )
        )
        cart.updated_at = datetime.utcnow()
        self._cart_repo.save(cart)
        return Result.success(self._cart_to_response(cart))

    def _cart_to_response(self, cart: Cart) -> CartResponse:
        return CartResponse(
            id=cart.id,
            items=[
                CartItemResponse(
                    product_id=i.product_id,
                    quantity=i.quantity,
                    unit_price=str(i.unit_price.amount),
                    line_total=str(i.line_total.amount),
                )
                for i in cart.items
            ],
            total=str(sum(i.line_total.amount for i in cart.items)),
        )


class RemoveFromCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self._cart_repo = cart_repo

    def execute(
        self, cart_id: uuid.UUID, product_id: uuid.UUID | None = None, clear: bool = False
    ) -> Result[CartResponse, str]:
        cart = self._cart_repo.find_by_id(cart_id)
        if cart is None:
            return Result.failure("Cart not found")

        if clear:
            cart.items.clear()
        elif product_id:
            cart.items = [i for i in cart.items if i.product_id != product_id]

        cart.updated_at = datetime.utcnow()
        self._cart_repo.save(cart)
        return Result.success(
            CartResponse(
                id=cart.id,
                items=[
                    CartItemResponse(
                        product_id=i.product_id,
                        quantity=i.quantity,
                        unit_price=str(i.unit_price.amount),
                        line_total=str(i.line_total.amount),
                    )
                    for i in cart.items
                ],
                total=str(sum(i.line_total.amount for i in cart.items)),
            )
        )


class GetCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self._cart_repo = cart_repo

    def execute(self, cart_id: uuid.UUID) -> Result[CartResponse, str]:
        cart = self._cart_repo.find_by_id(cart_id)
        if cart is None:
            return Result.failure("Cart not found")
        return Result.success(
            CartResponse(
                id=cart.id,
                items=[
                    CartItemResponse(
                        product_id=i.product_id,
                        quantity=i.quantity,
                        unit_price=str(i.unit_price.amount),
                        line_total=str(i.line_total.amount),
                    )
                    for i in cart.items
                ],
                total=str(sum(i.line_total.amount for i in cart.items)),
            )
        )


class MergeCartOnLoginUseCase:
    def __init__(self, cart_repo: CartRepository):
        self._cart_repo = cart_repo

    def execute(self, user_id: uuid.UUID, session_id: str) -> Result[CartResponse, str]:
        anon_cart = self._cart_repo.find_by_session_id(session_id)
        user_cart = self._cart_repo.find_by_user_id(user_id)

        if anon_cart is None and user_cart is None:
            return Result.failure("No cart to merge")

        if anon_cart is None and user_cart:
            return Result.success(
                CartResponse(
                    id=user_cart.id,
                    items=[
                        CartItemResponse(
                            product_id=i.product_id,
                            quantity=i.quantity,
                            unit_price=str(i.unit_price.amount),
                            line_total=str(i.line_total.amount),
                        )
                        for i in user_cart.items
                    ],
                    total=str(sum(i.line_total.amount for i in user_cart.items)),
                )
            )

        if user_cart is None and anon_cart:
            anon_cart.user_id = user_id
            anon_cart.session_id = None
            anon_cart.updated_at = datetime.utcnow()
            self._cart_repo.save(anon_cart)
            return Result.success(
                CartResponse(
                    id=anon_cart.id,
                    items=[
                        CartItemResponse(
                            product_id=i.product_id,
                            quantity=i.quantity,
                            unit_price=str(i.unit_price.amount),
                            line_total=str(i.line_total.amount),
                        )
                        for i in anon_cart.items
                    ],
                    total=str(sum(i.line_total.amount for i in anon_cart.items)),
                )
            )

        for anon_item in anon_cart.items:
            existing = next((i for i in user_cart.items if i.product_id == anon_item.product_id), None)
            if existing:
                user_cart.items.remove(existing)
                anon_item = CartItem(
                    product_id=anon_item.product_id,
                    quantity=existing.quantity + anon_item.quantity,
                    unit_price=anon_item.unit_price,
                )
            user_cart.items.append(anon_item)

        user_cart.updated_at = datetime.utcnow()
        self._cart_repo.save(user_cart)
        self._cart_repo.delete(anon_cart.id)

        return Result.success(
            CartResponse(
                id=user_cart.id,
                items=[
                    CartItemResponse(
                        product_id=i.product_id,
                        quantity=i.quantity,
                        unit_price=str(i.unit_price.amount),
                        line_total=str(i.line_total.amount),
                    )
                    for i in user_cart.items
                ],
                total=str(sum(i.line_total.amount for i in user_cart.items)),
            )
        )
