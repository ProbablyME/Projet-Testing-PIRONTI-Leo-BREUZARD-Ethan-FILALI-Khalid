from mybudget.services.exports import export_csv
from mybudget.domain.models import Transaction
from datetime import date
import os


def test_export_creates_file(tmp_path):
    file = tmp_path / "out.csv"

    transactions = [
        Transaction(1, 10, "Test", date.today(), "expense")
    ]

    export_csv(transactions, file)

    assert file.exists()
