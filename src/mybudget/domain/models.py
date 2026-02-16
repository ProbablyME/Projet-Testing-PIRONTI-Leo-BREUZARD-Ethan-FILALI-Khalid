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
