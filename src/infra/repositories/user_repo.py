from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from src.application.ports.user_repository import UserRepository
from src.domain.entities.models import User
from src.domain.value_objects.common import EmailAddress
from src.framework.db.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, user: User) -> User:
        model = UserModel(
            id=str(user.id),
            email=str(user.email),
            hashed_password=user.hashed_password,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._session.add(model)
        self._session.commit()
        return self._to_domain(model)

    def find_by_email(self, email: str) -> User | None:
        model = self._session.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(model) if model else None

    def find_by_id(self, user_id: uuid.UUID) -> User | None:
        model = self._session.query(UserModel).filter(UserModel.id == str(user_id)).first()
        return self._to_domain(model) if model else None

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=uuid.UUID(model.id),
            email=EmailAddress(model.email),
            hashed_password=model.hashed_password,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
