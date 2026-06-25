from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session, selectinload

from src.application.ports.cart_repository import CartRepository
from src.domain.entities.models import Cart, CartItem
from src.domain.value_objects.common import Money
from src.framework.db.models import CartItemModel, CartModel


class SQLAlchemyCartRepository(CartRepository):
    def __init__(self, session: Session):
        self._session = session

    def _load_cart(self, cart_id: str) -> CartModel | None:
        return (
            self._session.query(CartModel)
            .options(selectinload(CartModel.items))
            .filter(CartModel.id == cart_id)
            .first()
        )

    def create(self, cart: Cart) -> Cart:
        model = CartModel(
            id=str(cart.id),
            user_id=str(cart.user_id) if cart.user_id else None,
            session_id=cart.session_id,
            created_at=cart.created_at,
            updated_at=cart.updated_at,
        )
        self._session.add(model)
        for item in cart.items:
            self._session.add(
                CartItemModel(
                    cart_id=str(cart.id),
                    product_id=str(item.product_id),
                    quantity=item.quantity,
                    unit_price=float(item.unit_price.amount),
                )
            )
        self._session.commit()
        return self._to_domain(model)

    def find_by_id(self, cart_id: uuid.UUID) -> Cart | None:
        model = self._load_cart(str(cart_id))
        return self._to_domain(model) if model else None

    def find_by_user_id(self, user_id: uuid.UUID) -> Cart | None:
        model = (
            self._session.query(CartModel)
            .options(selectinload(CartModel.items))
            .filter(CartModel.user_id == str(user_id))
            .first()
        )
        return self._to_domain(model) if model else None

    def find_by_session_id(self, session_id: str) -> Cart | None:
        model = (
            self._session.query(CartModel)
            .options(selectinload(CartModel.items))
            .filter(CartModel.session_id == session_id)
            .first()
        )
        return self._to_domain(model) if model else None

    def save(self, cart: Cart) -> None:
        model = self._load_cart(str(cart.id))
        if not model:
            return
        model.user_id = str(cart.user_id) if cart.user_id else None
        model.session_id = cart.session_id
        model.updated_at = cart.updated_at

        existing = {i.product_id: i for i in model.items}
        updated_ids = {str(i.product_id) for i in cart.items}

        for item_model in model.items:
            if item_model.product_id not in updated_ids:
                self._session.delete(item_model)

        for item in cart.items:
            pid = str(item.product_id)
            if pid in existing:
                existing[pid].quantity = item.quantity
                existing[pid].unit_price = float(item.unit_price.amount)
            else:
                self._session.add(
                    CartItemModel(
                        cart_id=str(cart.id),
                        product_id=pid,
                        quantity=item.quantity,
                        unit_price=float(item.unit_price.amount),
                    )
                )
        self._session.commit()

    def delete(self, cart_id: uuid.UUID) -> None:
        self._session.query(CartItemModel).filter(CartItemModel.cart_id == str(cart_id)).delete()
        self._session.query(CartModel).filter(CartModel.id == str(cart_id)).delete()
        self._session.commit()

    @staticmethod
    def _to_domain(model: CartModel) -> Cart:
        return Cart(
            id=uuid.UUID(model.id),
            user_id=uuid.UUID(model.user_id) if model.user_id else None,
            session_id=model.session_id,
            items=[
                CartItem(
                    product_id=uuid.UUID(i.product_id),
                    quantity=i.quantity,
                    unit_price=Money(amount=Decimal(str(i.unit_price))),
                )
                for i in model.items
            ],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
