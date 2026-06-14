from __future__ import annotations

import dataclasses
from typing import Generic, TypeVar, final

T = TypeVar("T")
E = TypeVar("E")


@final
@dataclasses.dataclass(frozen=True)
class Result(Generic[T, E]):
    value: T | None = dataclasses.field(default=None)
    error: E | None = dataclasses.field(default=None)

    def __post_init__(self) -> None:
        if self.value is not None and self.error is not None:
            raise ValueError("Result cannot have both value and error")
        if self.value is None and self.error is None:
            raise ValueError("Result must have either value or error")

    @staticmethod
    def success(value: T) -> Result[T, E]:
        return Result(value=value, error=None)

    @staticmethod
    def failure(error: E) -> Result[T, E]:
        return Result(value=None, error=error)

    @property
    def is_success(self) -> bool:
        return self.value is not None

    @property
    def is_failure(self) -> bool:
        return self.error is not None

    def unwrap(self) -> T:
        if self.value is None:
            raise ValueError(f"Called unwrap on failure result: {self.error}")
        return self.value

    def unwrap_error(self) -> E:
        if self.error is None:
            raise ValueError(f"Called unwrap_error on success result: {self.value}")
        return self.error

    def map(self, fn):
        if self.is_success:
            return Result.success(fn(self.value))
        return Result.failure(self.error)
