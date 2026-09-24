# Module 6 – Python Capstone Project Learning Notes

## Day 26 – Application Design

A capstone project should combine previously learned programming concepts into one practical application.

The Expense Tracker uses a modular structure:

- `app.py` – application entry point
- `routes.py` – API routes
- `database.py` – SQLite connection and schema initialization
- `models.py` – transaction data model
- `auth.py` – authentication utilities
- `utils.py` – validation
- `logger.py` – application logging

This separation makes the application easier to understand and maintain.

## Day 27 – Database and CRUD

The project uses SQLite for persistent storage.

The application has two main tables:

### Users

Stores user account information.

### Transactions

Stores income and expense records connected to a user.

CRUD operations are implemented for transactions:

- Create – add transaction
- Read – view transactions
- Update – edit transaction
- Delete – remove transaction

## Day 28 – Authentication and Exception Safety

Users can register and log in.

After login, the application generates a token. Protected transaction endpoints require the token.

The application validates:

- Required fields
- Transaction type
- Amount
- Category
- Date format

Invalid requests return appropriate error responses instead of being stored.

## Day 29 – Logging and Testing

The application uses Python's `logging` module.

Logs are stored in:

`logs/app.log`

Pytest is used for automated testing.

Tests can verify registration, login, protected endpoints and transaction operations.

Run tests:

```bash
pytest
```

## Day 30 – Documentation and Deployment

The README documents:

- Project overview
- Features
- Architecture
- Setup
- API endpoints
- Database schema
- Authentication
- Testing
- Logging
- Deployment considerations

The application can be deployed to a Python-compatible hosting platform after configuring a production server.

## Final Learning Outcome

The capstone demonstrates how to build a complete Python application using modular design, Flask, REST APIs, SQLite, SQL CRUD, authentication, validation, logging, testing and documentation.
