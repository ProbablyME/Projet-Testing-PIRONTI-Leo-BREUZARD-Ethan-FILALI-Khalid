"""
Feature: Filtre des transactions par type
  En tant qu'utilisateur,
  je souhaite filtrer mes transactions par type (revenu ou dépense),
  afin de consulter uniquement mes revenus ou mes dépenses.

  Scenario: Afficher uniquement les dépenses
    Given un revenu de 1500 EUR et une dépense de 50 EUR
    When je filtre par type "expense"
    Then je ne vois que la dépense de 50 EUR
"""

from mybudget.infra.memory import InMemoryTransactionRepository
from mybudget.domain.models import Transaction
from datetime import date


def test_filtrer_depenses_uniquement():
    # Given un revenu de 1500 EUR et une dépense de 50 EUR
    repo = InMemoryTransactionRepository()
    repo.add(Transaction(1, 1500, "Salaire", date(2026, 1, 1), "income"))
    repo.add(Transaction(2, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"))

    # When je filtre par type "expense"
    result = repo.filter_by_type("expense")

    # Then je ne vois que la dépense de 50 EUR
    assert len(result) == 1
    assert result[0].amount == 50
    assert result[0].type == "expense"
