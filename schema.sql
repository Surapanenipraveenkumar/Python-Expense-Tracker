CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income','expense')),
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    description TEXT,
    transaction_date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
