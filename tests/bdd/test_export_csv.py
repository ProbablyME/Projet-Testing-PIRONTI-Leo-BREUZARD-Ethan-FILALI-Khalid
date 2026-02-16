"""
Feature: Export des transactions au format CSV
  En tant qu'utilisateur,
  je souhaite exporter mes transactions en CSV,
  afin de les consulter dans un tableur.

  Scenario: Exporter deux transactions en CSV
    Given deux transactions enregistrées
    When j'exporte en CSV
    Then le fichier contient un en-tête et deux lignes de données
"""

from mybudget.services.exports import export_csv
from mybudget.domain.models import Transaction
from datetime import date


def test_export_csv_contenu(tmp_path):
    # Given deux transactions enregistrées
    transactions = [
        Transaction(1, 50, "Courses", date(2026, 1, 10), "expense", "alimentation"),
        Transaction(2, 1500, "Salaire", date(2026, 1, 1), "income", "autre"),
    ]

    # When j'exporte en CSV
    file = tmp_path / "export.csv"
    export_csv(transactions, file)

    # Then le fichier contient un en-tête et deux lignes de données
    lines = file.read_text().strip().split("\n")
    assert len(lines) == 3
    assert "id,amount,description,date,type,category" in lines[0]
    assert "Courses" in lines[1]
    assert "Salaire" in lines[2]
