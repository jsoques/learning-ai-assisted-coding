from __future__ import annotations

import dataclasses
import uuid
from datetime import datetime
from decimal import Decimal


@dataclasses.dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class TokenResponse:
    access_token: str
    token_type: str = "bearer"


@dataclasses.dataclass(frozen=True)
class UserResponse:
    id: uuid.UUID
    email: str
    role: str
    created_at: datetime


@dataclasses.dataclass(frozen=True)
class CreateProductRequest:
    sku: str
    name: str
    description: str
    price: Decimal
    category_id: uuid.UUID


@dataclasses.dataclass(frozen=True)
class UpdateProductRequest:
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    category_id: uuid.UUID | None = None
    status: str | None = None


@dataclasses.dataclass(frozen=True)
class ProductResponse:
    id: uuid.UUID
    sku: str
    name: str
    description: str
    price: str
    category_id: uuid.UUID
    status: str
    available_stock: int
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass(frozen=True)
class CategoryRequest:
    name: str
    description: str


@dataclasses.dataclass(frozen=True)
class CategoryResponse:
    id: uuid.UUID
    name: str
    description: str


@dataclasses.dataclass(frozen=True)
class AddCartItemRequest:
    product_id: uuid.UUID
    quantity: int


@dataclasses.dataclass(frozen=True)
class CartItemResponse:
    product_id: uuid.UUID
    quantity: int
    unit_price: str
    line_total: str


@dataclasses.dataclass(frozen=True)
class CartResponse:
    id: uuid.UUID
    items: list[CartItemResponse]
    total: str


@dataclasses.dataclass(frozen=True)
class OrderLineItemResponse:
    product_id: uuid.UUID
    product_name: str
    quantity: int
    unit_price: str
    line_total: str


@dataclasses.dataclass(frozen=True)
class OrderResponse:
    id: uuid.UUID
    user_id: uuid.UUID
    line_items: list[OrderLineItemResponse]
    status: str
    total: str
    created_at: datetime
    updated_at: datetime


@dataclasses.dataclass(frozen=True)
class TransitionOrderStatusRequest:
    status: str


@dataclasses.dataclass(frozen=True)
class InventoryResponse:
    product_id: uuid.UUID
    on_hand: int
    reserved: int
    available: int
    low_stock_threshold: int
    is_low_stock: bool


@dataclasses.dataclass(frozen=True)
class RestockRequest:
    quantity: int


@dataclasses.dataclass(frozen=True)
class PaginatedResponse:
    items: list
    total: int
    page: int
    per_page: int
    total_pages: int
