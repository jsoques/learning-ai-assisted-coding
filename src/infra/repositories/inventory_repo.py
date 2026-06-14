from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from src.application.ports.inventory_repository import InventoryRepository
from src.domain.entities.models import InventoryItem, RestockEvent
from src.framework.db.models import InventoryModel, RestockEventModel
from src.framework.db.session import SessionLocal


class SQLAlchemyInventoryRepository(InventoryRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_product_id(self, product_id: uuid.UUID) -> InventoryItem | None:
        model = self._session.query(InventoryModel).filter(InventoryModel.product_id == str(product_id)).first()
        return self._to_domain(model) if model else None

    def save(self, item: InventoryItem) -> None:
        model = self._session.query(InventoryModel).filter(InventoryModel.product_id == str(item.product_id)).first()
        if model:
            model.on_hand = item.on_hand
            model.reserved = item.reserved
            model.low_stock_threshold = item.low_stock_threshold
        else:
            self._session.add(
                InventoryModel(
                    product_id=str(item.product_id),
                    on_hand=item.on_hand,
                    reserved=item.reserved,
                    low_stock_threshold=item.low_stock_threshold,
                )
            )
        self._session.commit()

    def reserve(self, product_id: uuid.UUID, quantity: int) -> InventoryItem:
        model = self._session.query(InventoryModel).filter(InventoryModel.product_id == str(product_id)).first()
        if model:
            model.reserved += quantity
            self._session.commit()
        return self._to_domain(model)

    def release(self, product_id: uuid.UUID, quantity: int) -> InventoryItem:
        model = self._session.query(InventoryModel).filter(InventoryModel.product_id == str(product_id)).first()
        if model:
            model.reserved = max(0, model.reserved - quantity)
            self._session.commit()
        return self._to_domain(model)

    def record_restock(self, event: RestockEvent) -> InventoryItem:
        model = self._session.query(InventoryModel).filter(InventoryModel.product_id == str(event.product_id)).first()
        if model:
            model.on_hand += event.quantity
            self._session.commit()
        self._session.add(
            RestockEventModel(
                product_id=str(event.product_id),
                quantity=event.quantity,
                timestamp=event.timestamp,
            )
        )
        self._session.commit()
        return self._to_domain(model)

    def _to_domain(self, model: InventoryModel) -> InventoryItem:
        return InventoryItem(
            product_id=uuid.UUID(model.product_id),
            on_hand=model.on_hand,
            reserved=model.reserved,
            low_stock_threshold=model.low_stock_threshold,
        )
