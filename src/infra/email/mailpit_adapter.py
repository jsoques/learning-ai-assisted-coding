from __future__ import annotations

import httpx

from src.application.ports.email_port import EmailPort


class MailpitEmailAdapter(EmailPort):
    _base_url = "http://localhost:8025"

    def send_order_confirmation(self, to_email: str, order_id: str, total: float) -> None:
        subject = f"Order Confirmation - {order_id}"
        body = f"Your order {order_id} has been created. Total: ${total:.2f}"
        self._send(to_email, subject, body)

    def send_shipping_notification(self, to_email: str, order_id: str) -> None:
        subject = f"Order Shipped - {order_id}"
        body = f"Your order {order_id} has been shipped!"
        self._send(to_email, subject, body)

    def send_low_stock_alert(self, to_email: str, product_name: str, sku: str, available: int) -> None:
        subject = f"Low Stock Alert - {product_name}"
        body = f"Product '{product_name}' (SKU: {sku}) is low on stock. Available: {available}"
        self._send(to_email, subject, body)

    def _send(self, to_email: str, subject: str, body: str) -> None:
        try:
            with httpx.Client() as client:
                client.post(
                    f"{self._base_url}/api/v1/send",
                    json={
                        "To": [{"Name": "", "Address": to_email}],
                        "Subject": subject,
                        "TextBody": body,
                    },
                )
        except httpx.RequestError:
            pass
