import pytest
import os
from datetime import date
from mybudget.domain.models import Transaction, Budget


@pytest.fixture
def tmp_data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("mybudget.infra.json_storage.DATA_DIR", str(tmp_path))
    monkeypatch.setattr("mybudget.infra.json_storage.TRANSACTIONS_FILE", str(tmp_path / "transactions.json"))
    monkeypatch.setattr("mybudget.infra.json_storage.BUDGETS_FILE", str(tmp_path / "budgets.json"))
    return tmp_path


def test_add_and_list_transactions(tmp_data_dir):
    from mybudget.infra.json_storage import JsonTransactionRepository
    repo = JsonTransactionRepository()
    repo.add(Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"))
    repo.add(Transaction(2, 1500, "Salaire", date(2026, 1, 1), "income"))

    result = repo.list()
    assert len(result) == 2
    assert result[0].description == "Courses"
    assert result[1].amount == 1500


def test_persistence_between_instances(tmp_data_dir):
    from mybudget.infra.json_storage import JsonTransactionRepository
    repo1 = JsonTransactionRepository()
    repo1.add(Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"))

    repo2 = JsonTransactionRepository()
    assert len(repo2.list()) == 1


def test_delete_transaction(tmp_data_dir):
    from mybudget.infra.json_storage import JsonTransactionRepository
    repo = JsonTransactionRepository()
    repo.add(Transaction(1, 50, "Courses", date(2026, 1, 10), "expense"))
    repo.delete(1)
    assert len(repo.list()) == 0


def test_update_transaction(tmp_data_dir):
    from mybudget.infra.json_storage import JsonTransactionRepository
    repo = JsonTransactionRepository()
    repo.add(Transaction(1, 50, "Courses", date(2026, 1, 10), "expense"))
    repo.update(1, amount=60)
    assert repo.list()[0].amount == 60


def test_filter_by_category(tmp_data_dir):
    from mybudget.infra.json_storage import JsonTransactionRepository
    repo = JsonTransactionRepository()
    repo.add(Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"))
    repo.add(Transaction(2, 100, "Loyer", date(2026, 1, 1), "expense", "logement"))

    result = repo.filter_by_category("alimentation")
    assert len(result) == 1


def test_filter_by_period(tmp_data_dir):
    from mybudget.infra.json_storage import JsonTransactionRepository
    repo = JsonTransactionRepository()
    repo.add(Transaction(1, 50, "Jan", date(2026, 1, 15), "expense"))
    repo.add(Transaction(2, 30, "Mar", date(2026, 3, 10), "expense"))

    result = repo.filter_by_period(date(2026, 1, 1), date(2026, 1, 31))
    assert len(result) == 1


def test_budget_set_and_get(tmp_data_dir):
    from mybudget.infra.json_storage import JsonBudgetRepository
    repo = JsonBudgetRepository()
    repo.set(Budget("alimentation", 300, 1, 2026))

    result = repo.get("alimentation", 1, 2026)
    assert result.amount == 300


def test_budget_persistence(tmp_data_dir):
    from mybudget.infra.json_storage import JsonBudgetRepository
    repo1 = JsonBudgetRepository()
    repo1.set(Budget("alimentation", 300, 1, 2026))

    repo2 = JsonBudgetRepository()
    assert repo2.get("alimentation", 1, 2026).amount == 300


def test_budget_replace_existing(tmp_data_dir):
    from mybudget.infra.json_storage import JsonBudgetRepository
    repo = JsonBudgetRepository()
    repo.set(Budget("alimentation", 300, 1, 2026))
    repo.set(Budget("alimentation", 400, 1, 2026))

    assert repo.get("alimentation", 1, 2026).amount == 400
    assert len(repo.list()) == 1
