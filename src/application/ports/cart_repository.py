from __future__ import annotations

import abc
import uuid

from src.domain.entities.models import Cart


class CartRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, cart: Cart) -> Cart: ...

    @abc.abstractmethod
    def find_by_id(self, cart_id: uuid.UUID) -> Cart | None: ...

    @abc.abstractmethod
    def find_by_user_id(self, user_id: uuid.UUID) -> Cart | None: ...

    @abc.abstractmethod
    def find_by_session_id(self, session_id: str) -> Cart | None: ...

    @abc.abstractmethod
    def save(self, cart: Cart) -> None: ...

    @abc.abstractmethod
    def delete(self, cart_id: uuid.UUID) -> None: ...
