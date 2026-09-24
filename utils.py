from datetime import datetime

def validate_transaction(data):
    required = ["transaction_type", "category", "amount", "transaction_date"]

    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    missing = [field for field in required if field not in data]
    if missing:
        return f"Missing fields: {', '.join(missing)}"

    if data["transaction_type"] not in ("income", "expense"):
        return "transaction_type must be income or expense."

    if not isinstance(data["category"], str) or not data["category"].strip():
        return "Category is required."

    try:
        amount = float(data["amount"])
        if amount <= 0:
            return "Amount must be greater than zero."
    except (TypeError, ValueError):
        return "Amount must be a valid number."

    try:
        datetime.strptime(data["transaction_date"], "%Y-%m-%d")
    except (TypeError, ValueError):
        return "transaction_date must use YYYY-MM-DD format."

    return None
