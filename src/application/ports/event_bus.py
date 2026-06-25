from __future__ import annotations

import abc

from src.domain.events.events import DomainEvent


class EventBus(abc.ABC):
    @abc.abstractmethod
    def publish(self, event: DomainEvent) -> None: ...
