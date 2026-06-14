from __future__ import annotations

import abc


class EmailPort(abc.ABC):
    @abc.abstractmethod
    def send_order_confirmation(self, to_email: str, order_id: str, total: float) -> None: ...

    @abc.abstractmethod
    def send_shipping_notification(self, to_email: str, order_id: str) -> None: ...

    @abc.abstractmethod
    def send_low_stock_alert(
        self, to_email: str, product_name: str, sku: str, available: int
    ) -> None: ...
