import argparse
from mybudget.infra.memory import InMemoryTransactionRepository, InMemoryBudgetRepository
from mybudget.domain.models import Transaction, Budget
from mybudget.services.budgets import budget_status
from datetime import date


repo = InMemoryTransactionRepository()
budget_repo = InMemoryBudgetRepository()


def main():
    parser = argparse.ArgumentParser(description="MyBudget CLI")

    subparsers = parser.add_subparsers(dest="command")

    # ADD command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--description", type=str, required=True)
    add_parser.add_argument("--type", type=str, required=True)
    add_parser.add_argument("--category", type=str, default="autre")
    add_parser.add_argument("--date", type=str, default=None)

    # LIST command
    subparsers.add_parser("list")

    # BUDGET-SET command
    bs_parser = subparsers.add_parser("budget-set")
    bs_parser.add_argument("--category", type=str, required=True)
    bs_parser.add_argument("--amount", type=float, required=True)
    bs_parser.add_argument("--month", type=int, required=True)
    bs_parser.add_argument("--year", type=int, required=True)

    # BUDGET-STATUS command
    bst_parser = subparsers.add_parser("budget-status")
    bst_parser.add_argument("--category", type=str, required=True)
    bst_parser.add_argument("--month", type=int, required=True)
    bst_parser.add_argument("--year", type=int, required=True)

    args = parser.parse_args()

    if args.command == "add":
        transaction_date = date.fromisoformat(args.date) if args.date else date.today()
        transaction = Transaction(
            id=len(repo.list()) + 1,
            amount=args.amount,
            description=args.description,
            date=transaction_date,
            type=args.type,
            category=args.category,
        )
        repo.add(transaction)
        print("Transaction added.")

    elif args.command == "list":
        transactions = repo.list()
        for t in transactions:
            print(t)

    elif args.command == "budget-set":
        b = Budget(
            category=args.category,
            amount=args.amount,
            month=args.month,
            year=args.year,
        )
        budget_repo.set(b)
        print(f"Budget set: {args.amount} for {args.category} ({args.month}/{args.year})")

    elif args.command == "budget-status":
        b = budget_repo.get(args.category, args.month, args.year)
        if not b:
            print("No budget defined for this category/period.")
        else:
            status = budget_status(b, repo.list())
            print(f"Category: {status['category']}")
            print(f"Budget: {status['budget']}")
            print(f"Spent: {status['spent']}")
            print(f"Remaining: {status['remaining']}")
            print(f"Consumed: {status['percentage']}%")

    else:
        parser.print_help()
