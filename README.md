# Expense Tracker API

A FastAPI-based Expense Tracker backend application with authentication, expense management, budgeting, and analytics.

## Features

- User Authentication (JWT)
- Create / Update / Delete Expenses
- Categories Management
- Monthly Budgets
- Expense Analytics
- Filtering, Search, Pagination
- Recurring Expenses
- PostgreSQL Database
- Logging & Error Handling
- Deployed on Render

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Uvicorn
- Render Deployment

---

## API Documentation

Swagger Docs:

```text
(https://expense-tracker-t5im.onrender.com)```

---

## Installation

Clone repository:

```bash
git clone Expense_Tracker
```

Install dependencies:

```bash
pip install -r req.txt
```

Run server:

```bash
uvicorn main:app --reload
```

---

## Environment Variables

Create `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

---

## Deployment

Deployed using Render with PostgreSQL database.

---

## Future Improvements

- Docker
- Alembic Migrations
- Redis Caching
- Unit Testing
- CI/CD
- Role-Based Access
