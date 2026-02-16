"""
Feature: Suppression d'une transaction
  En tant qu'utilisateur,
  je souhaite pouvoir supprimer une transaction,
  afin de retirer une entrée erronée de mon historique.

  Scenario: Supprimer une transaction existante
    Given deux transactions enregistrées
    When je supprime la première transaction
    Then il ne reste qu'une seule transaction
"""

from mybudget.infra.memory import InMemoryTransactionRepository
from mybudget.domain.models import Transaction
from datetime import date


def test_supprimer_transaction():
    # Given deux transactions enregistrées
    repo = InMemoryTransactionRepository()
    repo.add(Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"))
    repo.add(Transaction(2, 100, "Loyer", date(2026, 1, 1), "expense", "logement"))

    # When je supprime la première transaction
    repo.delete(1)

    # Then il ne reste qu'une seule transaction
    assert len(repo.list()) == 1
    assert repo.list()[0].id == 2
