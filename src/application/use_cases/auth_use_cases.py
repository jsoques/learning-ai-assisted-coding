from __future__ import annotations

import uuid
from datetime import datetime

from src.application.dto.dtos import (
    LoginRequest,
    RegisterUserRequest,
    TokenResponse,
    UserResponse,
)
from src.application.ports.user_repository import UserRepository
from src.application.result import Result
from src.domain.entities.models import User
from src.domain.value_objects.common import EmailAddress
from src.framework.auth.jwt import hash_password, verify_password


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def execute(self, request: RegisterUserRequest) -> Result[UserResponse, str]:
        try:
            email = EmailAddress(request.email)
        except ValueError as e:
            return Result.failure(str(e))

        if len(request.password) < 8:
            return Result.failure("Password must be at least 8 characters")

        existing = self._user_repo.find_by_email(str(email))
        if existing is not None:
            return Result.failure("Email already registered")

        hashed = hash_password(request.password)
        now = datetime.utcnow()
        user = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hashed,
            role="customer",
            created_at=now,
            updated_at=now,
        )
        created = self._user_repo.create(user)
        return Result.success(
            UserResponse(id=created.id, email=str(created.email), role=created.role, created_at=created.created_at)
        )


class AuthenticateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def execute(self, request: LoginRequest) -> Result[User, str]:
        user = self._user_repo.find_by_email(request.email)
        if user is None:
            return Result.failure("Invalid email or password")
        if not verify_password(request.password, user.hashed_password):
            return Result.failure("Invalid email or password")
        return Result.success(user)
