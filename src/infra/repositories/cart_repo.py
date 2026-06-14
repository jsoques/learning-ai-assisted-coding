from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from src.application.ports.cart_repository import CartRepository
from src.domain.entities.models import Cart, CartItem
from src.domain.value_objects.common import Money
from src.framework.db.models import CartItemModel, CartModel
from src.framework.db.session import SessionLocal


class SQLAlchemyCartRepository(CartRepository):
    def __init__(self, session: Session):
        self._session = session

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
        model = self._session.query(CartModel).filter(CartModel.id == str(cart_id)).first()
        return self._to_domain(model) if model else None

    def find_by_user_id(self, user_id: uuid.UUID) -> Cart | None:
        model = self._session.query(CartModel).filter(CartModel.user_id == str(user_id)).first()
        return self._to_domain(model) if model else None

    def find_by_session_id(self, session_id: str) -> Cart | None:
        model = self._session.query(CartModel).filter(CartModel.session_id == session_id).first()
        return self._to_domain(model) if model else None

    def save(self, cart: Cart) -> None:
        model = self._session.query(CartModel).filter(CartModel.id == str(cart.id)).first()
        if model:
            model.user_id = str(cart.user_id) if cart.user_id else None
            model.session_id = cart.session_id
            model.updated_at = cart.updated_at
            self._session.query(CartItemModel).filter(CartItemModel.cart_id == str(cart.id)).delete()
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

    def delete(self, cart_id: uuid.UUID) -> None:
        self._session.query(CartItemModel).filter(CartItemModel.cart_id == str(cart_id)).delete()
        self._session.query(CartModel).filter(CartModel.id == str(cart_id)).delete()
        self._session.commit()

    def _to_domain(self, model: CartModel) -> Cart:
        item_models = self._session.query(CartItemModel).filter(CartItemModel.cart_id == model.id).all()
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
                for i in item_models
            ],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
