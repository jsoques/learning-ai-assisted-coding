from __future__ import annotations

import abc
import uuid

from src.domain.entities.models import Order


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, order: Order) -> Order: ...

    @abc.abstractmethod
    def find_by_id(self, order_id: uuid.UUID) -> Order | None: ...

    @abc.abstractmethod
    def find_by_user_id(
        self, user_id: uuid.UUID, status: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Order], int]: ...

    @abc.abstractmethod
    def update_status(self, order_id: uuid.UUID, status: str) -> Order: ...

    @abc.abstractmethod
    def list_all(
        self, status: str | None = None, page: int = 1, per_page: int = 20
    ) -> tuple[list[Order], int]: ...
