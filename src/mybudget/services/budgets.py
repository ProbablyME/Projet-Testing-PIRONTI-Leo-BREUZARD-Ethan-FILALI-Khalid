def calculate_balance(transactions):
    balance = 0
    for t in transactions:
        if t.type == "income":
            balance += t.amount
        else:
            balance -= t.amount
    return balance


def total_spent_by_category(transactions, category, month, year):
    total = 0
    for t in transactions:
        if t.type == "expense" and t.category == category and t.date.month == month and t.date.year == year:
            total += t.amount
    return total


def budget_status(budget, transactions):
    spent = total_spent_by_category(transactions, budget.category, budget.month, budget.year)
    remaining = budget.amount - spent
    percentage = (spent / budget.amount) * 100 if budget.amount > 0 else 0
    return {
        "category": budget.category,
        "budget": budget.amount,
        "spent": spent,
        "remaining": remaining,
        "percentage": round(percentage, 1),
    }
