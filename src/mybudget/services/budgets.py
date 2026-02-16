def calculate_balance(transactions):
    balance = 0
    for t in transactions:
        if t.type == "income":
            balance += t.amount
        else:
            balance -= t.amount
    return balance
