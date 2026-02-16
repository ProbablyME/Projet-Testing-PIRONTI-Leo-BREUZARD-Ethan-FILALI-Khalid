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
