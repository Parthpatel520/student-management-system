# Student Management System (FastAPI)

This project is a FastAPI-based backend for managing students, courses, enrollments, grades, and authentication.

## Features

- User registration and login with JWT access/refresh tokens
- OTP email verification
- Forgot/reset password flow
- Student management endpoints
- Course management endpoints
- Enrollment management endpoints
- Grade management with GPA summary

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (via `psycopg2-binary`)
- Pydantic Settings

## Project Structure

```text
app/
  main.py
  config.py
  database.py
  dependencies.py
  models/
  routers/
  schemas/
  utils/
alembic/
requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root.
4. Run database migrations:

```bash
alembic upgrade head
```

5. Start the server:

```bash
uvicorn app.main:app --reload
```


## API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Main Route Groups

- `/auth` - register, verify OTP, login, refresh, logout, password reset
- `/Student` - student profile operations
- `/Course` - course CRUD operations
- `/Enrollment` - enrollment operations
- `/grades` - grade CRUD and student grade summary

## Notes

- Keep your `.env` file private and never commit secrets.
- Some endpoints are role-protected (`admin`, `student`) using JWT auth.
