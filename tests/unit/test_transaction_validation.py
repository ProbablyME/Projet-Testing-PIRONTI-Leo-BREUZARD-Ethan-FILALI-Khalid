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
