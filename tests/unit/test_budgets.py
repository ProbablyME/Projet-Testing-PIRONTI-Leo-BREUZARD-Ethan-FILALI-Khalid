import pytest
from mybudget.domain.models import Transaction, Budget
from mybudget.domain.errors import ValidationError
from mybudget.services.budgets import total_spent_by_category, budget_status
from mybudget.infra.memory import InMemoryBudgetRepository
from datetime import date


def test_total_spent_by_category():
    transactions = [
        Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"),
        Transaction(2, 30, "Restaurant", date(2026, 1, 15), "expense", "alimentation"),
        Transaction(3, 100, "Loyer", date(2026, 1, 1), "expense", "logement"),
    ]
    total = total_spent_by_category(transactions, "alimentation", 1, 2026)
    assert total == 80


def test_total_spent_ignores_other_months():
    transactions = [
        Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"),
        Transaction(2, 30, "Courses", date(2026, 2, 10), "expense", "alimentation"),
    ]
    total = total_spent_by_category(transactions, "alimentation", 1, 2026)
    assert total == 50


def test_total_spent_ignores_income():
    transactions = [
        Transaction(1, 1500, "Salaire", date(2026, 1, 1), "income", "autre"),
        Transaction(2, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"),
    ]
    total = total_spent_by_category(transactions, "alimentation", 1, 2026)
    assert total == 50


def test_budget_status_under_budget():
    budget = Budget("alimentation", 300, 1, 2026)
    transactions = [
        Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"),
        Transaction(2, 30, "Restaurant", date(2026, 1, 15), "expense", "alimentation"),
    ]
    status = budget_status(budget, transactions)
    assert status["spent"] == 80
    assert status["remaining"] == 220
    assert status["percentage"] == 26.7


def test_budget_status_over_budget():
    budget = Budget("alimentation", 100, 1, 2026)
    transactions = [
        Transaction(1, 60, "Courses", date(2026, 1, 10), "expense", "alimentation"),
        Transaction(2, 50, "Restaurant", date(2026, 1, 15), "expense", "alimentation"),
    ]
    status = budget_status(budget, transactions)
    assert status["spent"] == 110
    assert status["remaining"] == -10
    assert status["percentage"] == 110.0


def test_budget_invalid_amount():
    with pytest.raises(ValidationError):
        Budget("alimentation", -100, 1, 2026)


def test_budget_invalid_category():
    with pytest.raises(ValidationError):
        Budget("inconnu", 100, 1, 2026)


def test_budget_invalid_month():
    with pytest.raises(ValidationError):
        Budget("alimentation", 100, 13, 2026)


def test_budget_repo_set_and_get():
    repo = InMemoryBudgetRepository()
    b = Budget("alimentation", 300, 1, 2026)
    repo.set(b)
    result = repo.get("alimentation", 1, 2026)
    assert result.amount == 300


def test_budget_repo_replaces_existing():
    repo = InMemoryBudgetRepository()
    repo.set(Budget("alimentation", 300, 1, 2026))
    repo.set(Budget("alimentation", 400, 1, 2026))
    result = repo.get("alimentation", 1, 2026)
    assert result.amount == 400
    assert len(repo.list()) == 1
