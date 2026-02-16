from dataclasses import dataclass
from datetime import date
from .errors import ValidationError


VALID_CATEGORIES = [
    "alimentation", "logement", "loisirs", "transports", "sante", "autre"
]


@dataclass
class Transaction:
    id: int
    amount: float
    description: str
    date: date
    type: str  # "income" or "expense"
    category: str = "autre"

    def __post_init__(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be positive")

        if self.type not in ["income", "expense"]:
            raise ValidationError("Invalid transaction type")

        if self.category not in VALID_CATEGORIES:
            raise ValidationError(f"Invalid category: {self.category}")


@dataclass
class Budget:
    category: str
    amount: float
    month: int  # 1-12
    year: int

    def __post_init__(self):
        if self.amount <= 0:
            raise ValidationError("Budget amount must be positive")

        if self.category not in VALID_CATEGORIES:
            raise ValidationError(f"Invalid category: {self.category}")

        if self.month < 1 or self.month > 12:
            raise ValidationError("Invalid month")
