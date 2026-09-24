from dataclasses import dataclass

@dataclass
class Transaction:
    user_id: int
    transaction_type: str
    category: str
    amount: float
    description: str
    transaction_date: str
