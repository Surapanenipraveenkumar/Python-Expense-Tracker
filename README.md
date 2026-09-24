# Python Expense Tracker

## Module 6 – Python Capstone Project

A portfolio-ready Python Expense Tracker built with Flask and SQLite. The project demonstrates modular architecture, REST APIs, authentication, CRUD operations, validation, exception-safe processing and application logging.

## Features

- User registration and login
- Token-based session authentication
- Add income and expense transactions
- View transaction history
- Update transactions
- Delete transactions
- Expense/income categories
- Financial summary
- SQLite database
- Input validation
- Logging
- Automated API tests
- Clean modular file structure

## Architecture

```text
Client
  |
  v
Flask Application
  |
  +--> Authentication
  |
  +--> Routes/API
  |       |
  |       +--> Validation
  |       +--> CRUD
  |       +--> Summary
  |
  +--> Database Layer
  |       |
  |       +--> SQLite
  |
  +--> Logging
```

## Setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Application:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/register` | Register user |
| POST | `/api/login` | Login |
| GET | `/api/transactions` | View transactions |
| POST | `/api/transactions` | Add transaction |
| PUT | `/api/transactions/<id>` | Update transaction |
| DELETE | `/api/transactions/<id>` | Delete transaction |
| GET | `/api/summary` | Income/expense summary |

## Example Registration

```json
{
  "name": "Praveen",
  "email": "praveen@example.com",
  "password": "password123"
}
```

## Example Transaction

```json
{
  "transaction_type": "expense",
  "category": "Food",
  "amount": 250,
  "description": "Lunch",
  "transaction_date": "2026-09-24"
}
```

## Authentication

After login, send the returned token using:

```text
Authorization: Bearer YOUR_TOKEN
```

The token is stored in memory for this educational project. Production applications should use a stronger authentication and token-management system.

## Database Schema

### users

- id
- name
- email
- password

### transactions

- id
- user_id
- transaction_type
- category
- amount
- description
- transaction_date

## Testing

```bash
pytest
```

## Logging

Application events are written to:

```text
logs/app.log
```

## Deployment

The application is Flask-based and can be deployed to a Python-compatible hosting platform. Configure the production server and environment variables according to the hosting provider before deployment.

## Capstone Learning Outcome

This project combines Python programming, modules, Flask, REST APIs, SQLite, SQL CRUD, authentication, validation, testing, logging and documentation into one complete application.
