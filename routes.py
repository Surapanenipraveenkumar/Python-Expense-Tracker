from flask import Blueprint, request, jsonify
from database import get_connection
from auth import hash_password, create_token
from utils import validate_transaction
from logger import setup_logger

api = Blueprint("api", __name__)
logger = setup_logger()
TOKENS = {}

@api.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400

    connection = get_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        connection.commit()
        user_id = cursor.lastrowid
    except Exception:
        connection.close()
        return jsonify({"error": "Email already registered"}), 409

    connection.close()
    logger.info("User registered: %s", email)
    return jsonify({"message": "Registration successful", "user_id": user_id}), 201

@api.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    connection = get_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, hash_password(password))
    ).fetchone()
    connection.close()

    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_token()
    TOKENS[token] = user["id"]

    return jsonify({"message": "Login successful", "token": token})

def current_user():
    token = request.headers.get("Authorization", "")
    if not token.startswith("Bearer "):
        return None
    return TOKENS.get(token[7:])

@api.get("/transactions")
def get_transactions():
    user_id = current_user()
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    connection = get_connection()
    rows = connection.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY transaction_date DESC, id DESC",
        (user_id,)
    ).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])

@api.post("/transactions")
def add_transaction():
    user_id = current_user()
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    error = validate_transaction(data)
    if error:
        return jsonify({"error": error}), 400

    connection = get_connection()
    cursor = connection.execute("""
        INSERT INTO transactions
        (user_id, transaction_type, category, amount, description, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        data["transaction_type"],
        data["category"].strip(),
        float(data["amount"]),
        data.get("description", ""),
        data["transaction_date"]
    ))
    connection.commit()
    transaction_id = cursor.lastrowid
    connection.close()

    logger.info("Transaction created: %s", transaction_id)
    return jsonify({"message": "Transaction added", "id": transaction_id}), 201

@api.put("/transactions/<int:transaction_id>")
def update_transaction(transaction_id):
    user_id = current_user()
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    error = validate_transaction(data)
    if error:
        return jsonify({"error": error}), 400

    connection = get_connection()
    cursor = connection.execute("""
        UPDATE transactions
        SET transaction_type = ?, category = ?, amount = ?, description = ?, transaction_date = ?
        WHERE id = ? AND user_id = ?
    """, (
        data["transaction_type"],
        data["category"].strip(),
        float(data["amount"]),
        data.get("description", ""),
        data["transaction_date"],
        transaction_id,
        user_id
    ))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify({"message": "Transaction updated"})

@api.delete("/transactions/<int:transaction_id>")
def delete_transaction(transaction_id):
    user_id = current_user()
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    connection = get_connection()
    cursor = connection.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user_id)
    )
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Transaction not found"}), 404

    logger.info("Transaction deleted: %s", transaction_id)
    return jsonify({"message": "Transaction deleted"})

@api.get("/summary")
def summary():
    user_id = current_user()
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    connection = get_connection()

    income = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM transactions WHERE user_id = ? AND transaction_type = 'income'",
        (user_id,)
    ).fetchone()["total"]

    expenses = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM transactions WHERE user_id = ? AND transaction_type = 'expense'",
        (user_id,)
    ).fetchone()["total"]

    connection.close()

    return jsonify({
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "balance": round(income - expenses, 2)
    })
