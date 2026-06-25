from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from src.application.dto.dtos import (
    CreateProductRequest,
    PaginatedResponse,
    ProductResponse,
    UpdateProductRequest,
)
from src.application.ports.product_repository import ProductRepository, CategoryRepository
from src.application.ports.inventory_repository import InventoryRepository
from src.application.result import Result
from src.domain.entities.models import InventoryItem, Product
from src.domain.value_objects.common import Money, ProductStatus, SKU


class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository):
        self._product_repo = product_repo
        self._category_repo = category_repo

    def execute(self, request: CreateProductRequest) -> Result[ProductResponse, str]:
        existing = self._product_repo.find_by_sku(request.sku)
        if existing is not None:
            return Result.failure("SKU already exists")

        category = self._category_repo.find_by_id(request.category_id)
        if category is None:
            return Result.failure("Category not found")

        try:
            price = Money(amount=request.price)
        except ValueError as e:
            return Result.failure(str(e))

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        product = Product(
            id=uuid.uuid4(),
            sku=SKU(request.sku),
            name=request.name,
            description=request.description,
            price=price,
            category_id=request.category_id,
            status=ProductStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        created = self._product_repo.create(product)
        return Result.success(self._to_response(created, 0))

    def _to_response(self, product: Product, stock: int) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            sku=product.sku,
            name=product.name,
            description=product.description,
            price=str(product.price.amount),
            category_id=product.category_id,
            status=product.status.value,
            available_stock=stock,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )


class ListProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    def execute(
        self,
        query: str | None = None,
        category_id: uuid.UUID | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Result[PaginatedResponse, str]:
        products, total = self._product_repo.search(
            query=query,
            category_id=category_id,
            price_min=price_min,
            price_max=price_max,
            page=page,
            per_page=per_page,
        )
        total_pages = max(1, (total + per_page - 1) // per_page)
        return Result.success(
            PaginatedResponse(
                items=[self._to_response(p, 0) for p in products],
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
            )
        )

    def _to_response(self, product: Product, stock: int) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            sku=product.sku,
            name=product.name,
            description=product.description,
            price=str(product.price.amount),
            category_id=product.category_id,
            status=product.status.value,
            available_stock=stock,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )


class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository, inventory_repo: InventoryRepository):
        self._product_repo = product_repo
        self._inventory_repo = inventory_repo

    def execute(self, product_id: uuid.UUID) -> Result[ProductResponse, str]:
        product = self._product_repo.find_by_id(product_id)
        if product is None:
            return Result.failure("Product not found")
        inv = self._inventory_repo.find_by_product_id(product_id)
        stock = inv.available if inv else 0
        return Result.success(
            ProductResponse(
                id=product.id,
                sku=product.sku,
                name=product.name,
                description=product.description,
                price=str(product.price.amount),
                category_id=product.category_id,
                status=product.status.value,
                available_stock=stock,
                created_at=product.created_at,
                updated_at=product.updated_at,
            )
        )


class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    def execute(self, product_id: uuid.UUID, request: UpdateProductRequest) -> Result[ProductResponse, str]:
        product = self._product_repo.find_by_id(product_id)
        if product is None:
            return Result.failure("Product not found")

        if request.sku is not None and request.sku != product.sku:
            existing = self._product_repo.find_by_sku(request.sku)
            if existing is not None:
                return Result.failure("SKU already exists")
            product.sku = SKU(request.sku)
        if request.name is not None:
            product.name = request.name
        if request.description is not None:
            product.description = request.description
        if request.price is not None:
            product.price = Money(amount=request.price)
        if request.category_id is not None:
            product.category_id = request.category_id
        if request.status is not None:
            product.status = ProductStatus(request.status)
        product.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

        updated = self._product_repo.update(product)
        return Result.success(
            ProductResponse(
                id=updated.id,
                sku=updated.sku,
                name=updated.name,
                description=updated.description,
                price=str(updated.price.amount),
                category_id=updated.category_id,
                status=updated.status.value,
                available_stock=0,
                created_at=updated.created_at,
                updated_at=updated.updated_at,
            )
        )


class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    def execute(self, product_id: uuid.UUID) -> Result[None, str]:
        product = self._product_repo.find_by_id(product_id)
        if product is None:
            return Result.failure("Product not found")
        self._product_repo.soft_delete(product_id)
        return Result.success(None)
