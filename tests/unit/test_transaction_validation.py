import pytest
from mybudget.domain.models import Transaction
from mybudget.domain.errors import ValidationError
from datetime import date


def test_negative_amount_raises():
    with pytest.raises(ValidationError):
        Transaction(
            id=1,
            amount=-10,
            description="Test",
            date=date.today(),
            type="expense",
        )


def test_zero_amount_raises():
    with pytest.raises(ValidationError):
        Transaction(
            id=1,
            amount=0,
            description="Test",
            date=date.today(),
            type="expense",
        )


def test_invalid_type_raises():
    with pytest.raises(ValidationError):
        Transaction(
            id=1,
            amount=10,
            description="Test",
            date=date.today(),
            type="invalid",
        )


def test_invalid_category_raises():
    with pytest.raises(ValidationError):
        Transaction(
            id=1,
            amount=10,
            description="Test",
            date=date.today(),
            type="expense",
            category="inconnu",
        )


def test_valid_transaction():
    t = Transaction(
        id=1,
        amount=50,
        description="Courses",
        date=date(2026, 1, 15),
        type="expense",
        category="alimentation",
    )
    assert t.amount == 50
    assert t.category == "alimentation"
