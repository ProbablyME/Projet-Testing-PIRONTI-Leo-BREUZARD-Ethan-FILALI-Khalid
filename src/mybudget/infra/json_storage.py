import json
import os
from datetime import date
from mybudget.domain.models import Transaction, Budget

DATA_DIR = os.path.join(os.path.expanduser("~"), ".mybudget")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.json")


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


class JsonTransactionRepository:
    def __init__(self):
        _ensure_dir()

    def _load(self):
        if not os.path.exists(TRANSACTIONS_FILE):
            return []
        with open(TRANSACTIONS_FILE, "r") as f:
            data = json.load(f)
        return [
            Transaction(
                id=d["id"],
                amount=d["amount"],
                description=d["description"],
                date=date.fromisoformat(d["date"]),
                type=d["type"],
                category=d.get("category", "autre"),
            )
            for d in data
        ]

    def _save(self, transactions):
        with open(TRANSACTIONS_FILE, "w") as f:
            json.dump(
                [
                    {
                        "id": t.id,
                        "amount": t.amount,
                        "description": t.description,
                        "date": t.date.isoformat(),
                        "type": t.type,
                        "category": t.category,
                    }
                    for t in transactions
                ],
                f,
                indent=2,
            )

    def add(self, transaction):
        transactions = self._load()
        transactions.append(transaction)
        self._save(transactions)

    def list(self):
        return self._load()

    def filter_by_type(self, type_):
        return [t for t in self._load() if t.type == type_]

    def filter_by_category(self, category):
        return [t for t in self._load() if t.category == category]

    def filter_by_period(self, start, end):
        return [t for t in self._load() if start <= t.date <= end]

    def update(self, id_, **kwargs):
        transactions = self._load()
        for t in transactions:
            if t.id == id_:
                for key, value in kwargs.items():
                    setattr(t, key, value)
        self._save(transactions)

    def delete(self, id_):
        transactions = [t for t in self._load() if t.id != id_]
        self._save(transactions)


class JsonBudgetRepository:
    def __init__(self):
        _ensure_dir()

    def _load(self):
        if not os.path.exists(BUDGETS_FILE):
            return []
        with open(BUDGETS_FILE, "r") as f:
            data = json.load(f)
        return [
            Budget(
                category=d["category"],
                amount=d["amount"],
                month=d["month"],
                year=d["year"],
            )
            for d in data
        ]

    def _save(self, budgets):
        with open(BUDGETS_FILE, "w") as f:
            json.dump(
                [
                    {
                        "category": b.category,
                        "amount": b.amount,
                        "month": b.month,
                        "year": b.year,
                    }
                    for b in budgets
                ],
                f,
                indent=2,
            )

    def set(self, budget):
        budgets = [
            b for b in self._load()
            if not (b.category == budget.category and b.month == budget.month and b.year == budget.year)
        ]
        budgets.append(budget)
        self._save(budgets)

    def get(self, category, month, year):
        for b in self._load():
            if b.category == category and b.month == month and b.year == year:
                return b
        return None

    def list(self):
        return self._load()
