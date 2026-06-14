from __future__ import annotations

import dataclasses
import uuid
from datetime import datetime


@dataclasses.dataclass(frozen=True)
class DomainEvent:
    event_id: uuid.UUID
    occurred_at: datetime


@dataclasses.dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    order_id: uuid.UUID
    user_id: uuid.UUID
    total: float


@dataclasses.dataclass(frozen=True)
class OrderCancelled(DomainEvent):
    order_id: uuid.UUID
    user_id: uuid.UUID


@dataclasses.dataclass(frozen=True)
class StockDepleted(DomainEvent):
    product_id: uuid.UUID
    sku: str
    available: int


@dataclasses.dataclass(frozen=True)
class LowStockAlert(DomainEvent):
    product_id: uuid.UUID
    sku: str
    available: int
    threshold: int
