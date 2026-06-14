from __future__ import annotations

import dataclasses
import uuid
from datetime import datetime

from src.domain.value_objects.common import EmailAddress, Money, OrderStatus, ProductStatus, SKU


@dataclasses.dataclass
class User:
    id: uuid.UUID
    email: EmailAddress
    hashed_password: str
    role: str
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass
class Category:
    id: uuid.UUID
    name: str
    description: str


@dataclasses.dataclass
class Product:
    id: uuid.UUID
    sku: SKU
    name: str
    description: str
    price: Money
    category_id: uuid.UUID
    status: ProductStatus
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass
class CartItem:
    product_id: uuid.UUID
    quantity: int
    unit_price: Money

    @property
    def line_total(self) -> Money:
        return self.unit_price * self.quantity


@dataclasses.dataclass
class Cart:
    id: uuid.UUID
    user_id: uuid.UUID | None
    session_id: str | None
    items: list[CartItem]
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass
class OrderLineItem:
    product_id: uuid.UUID
    product_name: str
    quantity: int
    unit_price: Money
    line_total: Money


@dataclasses.dataclass
class Order:
    id: uuid.UUID
    user_id: uuid.UUID
    line_items: list[OrderLineItem]
    status: OrderStatus
    total: Money
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass
class InventoryItem:
    product_id: uuid.UUID
    on_hand: int
    reserved: int
    low_stock_threshold: int

    @property
    def available(self) -> int:
        return self.on_hand - self.reserved

    @property
    def is_low_stock(self) -> bool:
        return self.available <= self.low_stock_threshold


@dataclasses.dataclass
class RestockEvent:
    product_id: uuid.UUID
    quantity: int
    timestamp: datetime
