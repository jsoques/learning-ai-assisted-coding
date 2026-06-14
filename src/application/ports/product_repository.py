from __future__ import annotations

import abc
import uuid

from src.domain.entities.models import Category, Product


class ProductRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, product: Product) -> Product: ...

    @abc.abstractmethod
    def find_by_id(self, product_id: uuid.UUID) -> Product | None: ...

    @abc.abstractmethod
    def find_by_sku(self, sku: str) -> Product | None: ...

    @abc.abstractmethod
    def search(
        self,
        query: str | None = None,
        category_id: uuid.UUID | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Product], int]: ...

    @abc.abstractmethod
    def update(self, product: Product) -> Product: ...

    @abc.abstractmethod
    def soft_delete(self, product_id: uuid.UUID) -> None: ...


class CategoryRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, category: Category) -> Category: ...

    @abc.abstractmethod
    def list_all(self) -> list[Category]: ...

    @abc.abstractmethod
    def find_by_id(self, category_id: uuid.UUID) -> Category | None: ...

    @abc.abstractmethod
    def update(self, category: Category) -> Category: ...
