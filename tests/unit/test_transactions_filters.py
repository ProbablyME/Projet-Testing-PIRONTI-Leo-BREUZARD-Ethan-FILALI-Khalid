from mybudget.infra.memory import InMemoryTransactionRepository
from mybudget.domain.models import Transaction
from datetime import date


def test_add_and_list_transactions():
    repo = InMemoryTransactionRepository()
    t = Transaction(1, 10, "Test", date.today(), "expense")
    repo.add(t)

    assert len(repo.list()) == 1


def test_filter_by_type():
    repo = InMemoryTransactionRepository()
    repo.add(Transaction(1, 100, "Salary", date.today(), "income"))
    repo.add(Transaction(2, 50, "Food", date.today(), "expense"))

    expenses = repo.filter_by_type("expense")

    assert len(expenses) == 1


def test_filter_by_category():
    repo = InMemoryTransactionRepository()
    repo.add(Transaction(1, 50, "Courses", date.today(), "expense", "alimentation"))
    repo.add(Transaction(2, 100, "Loyer", date.today(), "expense", "logement"))

    result = repo.filter_by_category("alimentation")

    assert len(result) == 1
    assert result[0].description == "Courses"


def test_filter_by_period():
    repo = InMemoryTransactionRepository()
    repo.add(Transaction(1, 50, "Jan", date(2026, 1, 15), "expense"))
    repo.add(Transaction(2, 30, "Feb", date(2026, 2, 10), "expense"))
    repo.add(Transaction(3, 20, "Mar", date(2026, 3, 5), "expense"))

    result = repo.filter_by_period(date(2026, 1, 1), date(2026, 1, 31))

    assert len(result) == 1
    assert result[0].description == "Jan"


def test_filter_by_period_multiple():
    repo = InMemoryTransactionRepository()
    repo.add(Transaction(1, 50, "Jan", date(2026, 1, 15), "expense"))
    repo.add(Transaction(2, 30, "Feb", date(2026, 2, 10), "expense"))

    result = repo.filter_by_period(date(2026, 1, 1), date(2026, 2, 28))

    assert len(result) == 2


def test_update_transaction():
    repo = InMemoryTransactionRepository()
    t = Transaction(1, 10, "Old", date.today(), "expense")
    repo.add(t)

    repo.update(1, amount=20)

    assert repo.list()[0].amount == 20


def test_delete_transaction():
    repo = InMemoryTransactionRepository()
    t = Transaction(1, 10, "Test", date.today(), "expense")
    repo.add(t)

    repo.delete(1)

    assert len(repo.list()) == 0
