from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.application.ports.product_repository import CategoryRepository, ProductRepository
from src.domain.entities.models import Category, Product
from src.domain.value_objects.common import Money, ProductStatus, SKU
from src.framework.db.models import CategoryModel, ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, product: Product) -> Product:
        model = ProductModel(
            id=str(product.id),
            sku=product.sku,
            name=product.name,
            description=product.description,
            price=float(product.price.amount),
            category_id=str(product.category_id),
            status=product.status.value,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
        self._session.add(model)
        self._session.commit()
        return self._to_domain(model)

    def find_by_id(self, product_id: uuid.UUID) -> Product | None:
        model = self._session.query(ProductModel).filter(ProductModel.id == str(product_id)).first()
        return self._to_domain(model) if model else None

    def find_by_sku(self, sku: str) -> Product | None:
        model = self._session.query(ProductModel).filter(ProductModel.sku == sku).first()
        return self._to_domain(model) if model else None

    def search(
        self,
        query: str | None = None,
        category_id: uuid.UUID | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Product], int]:
        q = self._session.query(ProductModel).filter(ProductModel.status == "active")
        if query:
            q = q.filter(
                or_(
                    ProductModel.name.ilike(f"%{query}%"),
                    ProductModel.description.ilike(f"%{query}%"),
                )
            )
        if category_id:
            q = q.filter(ProductModel.category_id == str(category_id))
        if price_min is not None:
            q = q.filter(ProductModel.price >= price_min)
        if price_max is not None:
            q = q.filter(ProductModel.price <= price_max)

        total = q.count()
        models = q.offset((page - 1) * per_page).limit(per_page).all()
        return [self._to_domain(m) for m in models], total

    def update(self, product: Product) -> Product:
        model = self._session.query(ProductModel).filter(ProductModel.id == str(product.id)).first()
        if model:
            model.sku = product.sku
            model.name = product.name
            model.description = product.description
            model.price = float(product.price.amount)
            model.category_id = str(product.category_id)
            model.status = product.status.value
            model.updated_at = product.updated_at
            self._session.commit()
        return product

    def soft_delete(self, product_id: uuid.UUID) -> None:
        model = self._session.query(ProductModel).filter(ProductModel.id == str(product_id)).first()
        if model:
            model.status = "inactive"
            self._session.commit()

    def _to_domain(self, model: ProductModel) -> Product:
        return Product(
            id=uuid.UUID(model.id),
            sku=SKU(model.sku),
            name=model.name,
            description=model.description,
            price=Money(amount=Decimal(str(model.price))),
            category_id=uuid.UUID(model.category_id),
            status=ProductStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, category: Category) -> Category:
        model = CategoryModel(
            id=str(category.id),
            name=category.name,
            description=category.description,
        )
        self._session.add(model)
        self._session.commit()
        return self._to_domain(model)

    def list_all(self) -> list[Category]:
        models = self._session.query(CategoryModel).all()
        return [self._to_domain(m) for m in models]

    def find_by_id(self, category_id: uuid.UUID) -> Category | None:
        model = self._session.query(CategoryModel).filter(CategoryModel.id == str(category_id)).first()
        return self._to_domain(model) if model else None

    def update(self, category: Category) -> Category:
        model = self._session.query(CategoryModel).filter(CategoryModel.id == str(category.id)).first()
        if model:
            model.name = category.name
            model.description = category.description
            self._session.commit()
        return category

    def _to_domain(self, model: CategoryModel) -> Category:
        return Category(
            id=uuid.UUID(model.id),
            name=model.name,
            description=model.description,
        )
