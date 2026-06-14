from __future__ import annotations

import dataclasses
import re
from decimal import Decimal
from enum import Enum
from typing import NewType


SKU = NewType("SKU", str)


@dataclasses.dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise ValueError("Amount cannot be negative")

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, multiplier: int) -> Money:
        return Money(amount=self.amount * multiplier, currency=self.currency)


@dataclasses.dataclass(frozen=True)
class EmailAddress:
    address: str

    def __post_init__(self) -> None:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.address):
            raise ValueError(f"Invalid email address: {self.address}")

    def __str__(self) -> str:
        return self.address


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def can_transition_to(self, target: OrderStatus) -> bool:
        transitions = {
            OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELLED},
            OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
            OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
            OrderStatus.DELIVERED: set(),
            OrderStatus.CANCELLED: set(),
        }
        return target in transitions[self]


class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
