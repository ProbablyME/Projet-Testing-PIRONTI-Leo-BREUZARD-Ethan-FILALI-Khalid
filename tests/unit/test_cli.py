import sys
import pytest
from unittest.mock import patch
from mybudget.cli.app import main, repo, budget_repo


@pytest.fixture(autouse=True)
def clean_repos():
    repo._transactions.clear()
    budget_repo._budgets.clear()
    yield
    repo._transactions.clear()
    budget_repo._budgets.clear()


def test_add_transaction(capsys):
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "50", "--description", "Courses", "--type", "expense", "--category", "alimentation", "--date", "2026-01-10"]):
        main()
    output = capsys.readouterr().out
    assert "Transaction added." in output
    assert len(repo.list()) == 1
    assert repo.list()[0].category == "alimentation"


def test_add_transaction_default_category(capsys):
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "10", "--description", "Test", "--type", "expense"]):
        main()
    assert repo.list()[0].category == "autre"


def test_list_transactions(capsys):
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "50", "--description", "Courses", "--type", "expense"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "list"]):
        main()
    output = capsys.readouterr().out
    assert "Courses" in output


def test_list_filter_by_category(capsys):
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "50", "--description", "Courses", "--type", "expense", "--category", "alimentation"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "100", "--description", "Loyer", "--type", "expense", "--category", "logement"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "list", "--category", "alimentation"]):
        main()
    output = capsys.readouterr().out
    assert "Courses" in output
    assert "Loyer" not in output


def test_list_filter_by_period(capsys):
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "50", "--description", "Jan", "--type", "expense", "--date", "2026-01-15"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "30", "--description", "Mar", "--type", "expense", "--date", "2026-03-10"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "list", "--from", "2026-01-01", "--to", "2026-01-31"]):
        main()
    output = capsys.readouterr().out
    assert "Jan" in output
    assert "Mar" not in output


def test_budget_set(capsys):
    with patch.object(sys, "argv", ["mybudget", "budget-set", "--category", "alimentation", "--amount", "300", "--month", "1", "--year", "2026"]):
        main()
    output = capsys.readouterr().out
    assert "Budget set" in output
    assert budget_repo.get("alimentation", 1, 2026) is not None


def test_budget_status(capsys):
    with patch.object(sys, "argv", ["mybudget", "budget-set", "--category", "alimentation", "--amount", "300", "--month", "1", "--year", "2026"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "add", "--amount", "80", "--description", "Courses", "--type", "expense", "--category", "alimentation", "--date", "2026-01-10"]):
        main()
    with patch.object(sys, "argv", ["mybudget", "budget-status", "--category", "alimentation", "--month", "1", "--year", "2026"]):
        main()
    output = capsys.readouterr().out
    assert "Spent: 80" in output
    assert "Remaining: 220" in output


def test_budget_status_no_budget(capsys):
    with patch.object(sys, "argv", ["mybudget", "budget-status", "--category", "alimentation", "--month", "1", "--year", "2026"]):
        main()
    output = capsys.readouterr().out
    assert "No budget defined" in output
