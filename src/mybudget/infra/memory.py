class InMemoryTransactionRepository:
    def __init__(self):
        self._transactions = []

    def add(self, transaction):
        self._transactions.append(transaction)

    def list(self):
        return self._transactions
