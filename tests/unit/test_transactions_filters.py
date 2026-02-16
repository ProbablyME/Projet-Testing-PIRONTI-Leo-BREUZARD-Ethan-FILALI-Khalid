from mybudget.infra.memory import InMemoryTransactionRepository
from mybudget.domain.models import Transaction
from datetime import date


def test_add_and_list_transactions():
    repo = InMemoryTransactionRepository()
    t = Transaction(1, 10, "Test", date.today(), "expense")
    repo.add(t)

    assert len(repo.list()) == 1
