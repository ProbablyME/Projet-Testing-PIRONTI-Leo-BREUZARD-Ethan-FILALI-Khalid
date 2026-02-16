from mybudget.domain.models import Transaction
from mybudget.services.budgets import calculate_balance
from datetime import date


def test_balance_calculation():
    transactions = [
        Transaction(1, 100, "Salary", date.today(), "income"),
        Transaction(2, 50, "Food", date.today(), "expense"),
    ]

    assert calculate_balance(transactions) == 50
