class InMemoryTransactionRepository:
    def __init__(self):
        self._transactions = []

    def add(self, transaction):
        self._transactions.append(transaction)

    def list(self):
        return self._transactions

    def filter_by_type(self, type_):
        return [t for t in self._transactions if t.type == type_]

    def update(self, id_, **kwargs):
        for t in self._transactions:
            if t.id == id_:
                for key, value in kwargs.items():
                    setattr(t, key, value)

    def delete(self, id_):
        self._transactions = [
            t for t in self._transactions if t.id != id_
        ]


class InMemoryBudgetRepository:
    def __init__(self):
        self._budgets = []

    def set(self, budget):
        # remplace si un budget existe déjà pour cette catégorie/mois/année
        self._budgets = [
            b for b in self._budgets
            if not (b.category == budget.category and b.month == budget.month and b.year == budget.year)
        ]
        self._budgets.append(budget)

    def get(self, category, month, year):
        for b in self._budgets:
            if b.category == category and b.month == month and b.year == year:
                return b
        return None

    def list(self):
        return self._budgets
