"""
Feature: Modification d'une transaction
  En tant qu'utilisateur,
  je souhaite pouvoir modifier une transaction existante,
  afin de corriger une erreur de saisie.

  Scenario: Modifier le montant d'une transaction
    Given une transaction de 50 EUR pour "Courses" en catégorie alimentation
    When je modifie le montant à 60 EUR
    Then la transaction affiche 60 EUR
"""

from mybudget.infra.memory import InMemoryTransactionRepository
from mybudget.domain.models import Transaction
from datetime import date


def test_modifier_montant_transaction():
    # Given une transaction de 50 EUR pour "Courses" en catégorie alimentation
    repo = InMemoryTransactionRepository()
    t = Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation")
    repo.add(t)

    # When je modifie le montant à 60 EUR
    repo.update(1, amount=60)

    # Then la transaction affiche 60 EUR
    assert repo.list()[0].amount == 60


def test_modifier_description_transaction():
    # Given une transaction avec description "Courses"
    repo = InMemoryTransactionRepository()
    t = Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation")
    repo.add(t)

    # When je modifie la description en "Courses Leclerc"
    repo.update(1, description="Courses Leclerc")

    # Then la description est "Courses Leclerc"
    assert repo.list()[0].description == "Courses Leclerc"
