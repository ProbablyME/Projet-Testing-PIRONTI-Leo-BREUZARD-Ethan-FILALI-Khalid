class InMemoryTransactionRepository:
    def __init__(self):
        self._transactions = []

    def add(self, transaction):
        self._transactions.append(transaction)

    def list(self):
        return self._transactions

    def filter_by_type(self, type_):
        return [t for t in self._transactions if t.type == type_]
