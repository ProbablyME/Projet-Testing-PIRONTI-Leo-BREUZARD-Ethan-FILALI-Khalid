import argparse
from mybudget.infra.memory import InMemoryTransactionRepository
from mybudget.domain.models import Transaction
from datetime import date


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

    args = parser.parse_args()

    repo = InMemoryTransactionRepository()

    if args.command == "add":
        transaction_date = date.fromisoformat(args.date) if args.date else date.today()
        transaction = Transaction(
            id=1,
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

    else:
        parser.print_help()
