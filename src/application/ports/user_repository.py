from __future__ import annotations

import abc
import uuid

from src.domain.entities.models import User


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, user: User) -> User: ...

    @abc.abstractmethod
    def find_by_email(self, email: str) -> User | None: ...

    @abc.abstractmethod
    def find_by_id(self, user_id: uuid.UUID) -> User | None: ...
