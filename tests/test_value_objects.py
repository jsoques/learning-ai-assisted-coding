from __future__ import annotations

from decimal import Decimal

import pytest

from src.domain.value_objects.common import EmailAddress, Money, OrderStatus, ProductStatus


class TestMoney:
    def test_create(self):
        m = Money(amount=Decimal("19.99"))
        assert m.amount == Decimal("19.99")
        assert m.currency == "USD"

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="negative"):
            Money(amount=Decimal("-1"))

    def test_addition(self):
        a = Money(Decimal("10"))
        b = Money(Decimal("5"))
        assert (a + b).amount == Decimal("15")

    def test_multiplication(self):
        m = Money(Decimal("10"))
        assert (m * 3).amount == Decimal("30")


class TestEmailAddress:
    def test_valid_email(self):
        email = EmailAddress("user@example.com")
        assert str(email) == "user@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValueError):
            EmailAddress("not-an-email")


class TestOrderStatus:
    def test_pending_to_paid(self):
        assert OrderStatus.PENDING.can_transition_to(OrderStatus.PAID)

    def test_pending_to_cancelled(self):
        assert OrderStatus.PENDING.can_transition_to(OrderStatus.CANCELLED)

    def test_delivered_cannot_transition(self):
        assert not OrderStatus.DELIVERED.can_transition_to(OrderStatus.SHIPPED)

    def test_cancelled_cannot_transition(self):
        assert not OrderStatus.CANCELLED.can_transition_to(OrderStatus.PENDING)


class TestProductStatus:
    def test_values(self):
        assert ProductStatus.ACTIVE.value == "active"
        assert ProductStatus.INACTIVE.value == "inactive"
