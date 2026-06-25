from __future__ import annotations

import logging

from src.application.ports.event_bus import EventBus
from src.domain.events.events import DomainEvent

logger = logging.getLogger("ecommerce.events")


class LoggingEventBus(EventBus):
    def publish(self, event: DomainEvent) -> None:
        logger.info("Domain event: %s", event)
