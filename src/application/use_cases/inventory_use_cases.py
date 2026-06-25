from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.application.dto.dtos import InventoryResponse, RestockRequest
from src.application.ports.inventory_repository import InventoryRepository
from src.application.result import Result
from src.domain.entities.models import InventoryItem, RestockEvent


class CheckInventoryUseCase:
    def __init__(self, inventory_repo: InventoryRepository):
        self._inventory_repo = inventory_repo

    def execute(self, product_id: uuid.UUID) -> Result[InventoryResponse, str]:
        item = self._inventory_repo.find_by_product_id(product_id)
        if item is None:
            return Result.failure("Inventory not found for product")
        return Result.success(
            InventoryResponse(
                product_id=item.product_id,
                on_hand=item.on_hand,
                reserved=item.reserved,
                available=item.available,
                low_stock_threshold=item.low_stock_threshold,
                is_low_stock=item.is_low_stock,
            )
        )


class RecordRestockUseCase:
    def __init__(self, inventory_repo: InventoryRepository):
        self._inventory_repo = inventory_repo

    def execute(self, product_id: uuid.UUID, request: RestockRequest) -> Result[InventoryResponse, str]:
        item = self._inventory_repo.find_by_product_id(product_id)
        if item is None:
            return Result.failure("Inventory not found for product")
        if request.quantity <= 0:
            return Result.failure("Restock quantity must be positive")

        event = RestockEvent(
            product_id=product_id,
            quantity=request.quantity,
            timestamp=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        updated = self._inventory_repo.record_restock(event)
        return Result.success(
            InventoryResponse(
                product_id=updated.product_id,
                on_hand=updated.on_hand,
                reserved=updated.reserved,
                available=updated.available,
                low_stock_threshold=updated.low_stock_threshold,
                is_low_stock=updated.is_low_stock,
            )
        )
