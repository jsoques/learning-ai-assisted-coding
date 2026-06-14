from __future__ import annotations

import abc
import uuid

from src.domain.entities.models import InventoryItem, RestockEvent


class InventoryRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_product_id(self, product_id: uuid.UUID) -> InventoryItem | None: ...

    @abc.abstractmethod
    def save(self, item: InventoryItem) -> None: ...

    @abc.abstractmethod
    def reserve(self, product_id: uuid.UUID, quantity: int) -> InventoryItem: ...

    @abc.abstractmethod
    def release(self, product_id: uuid.UUID, quantity: int) -> InventoryItem: ...

    @abc.abstractmethod
    def record_restock(self, event: RestockEvent) -> InventoryItem: ...
