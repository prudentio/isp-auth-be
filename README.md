# Auth Service - Setup and Run

This service is built using FastAPI with Python 3.11 and Poetry.

---

## Requirements

- Python 3.11  
- Poetry  
- PostgreSQL (local or Docker)
- RabbitMQ (message broker)

---

## Database Setup

Create database in PostgreSQL:

```sql
CREATE DATABASE auth_db;
```

## Environment Setup

Copy environment example file:
```cp .env.example .env```

Then fill in the required values inside .env

## Install Dependencies

Install all dependencies using Poetry:
```poetry
poetry install
```

## Activate Virtual Environment

You could use your generated venv like this in powershell
```
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& C:\Users\barra\AppData\Local\pypoetry\Cache\virtualenvs\fastapi-template-GKadvzmF-py3.11\Scripts\Activate.ps1)
```

## Run Application
```
fastapi dev app/main.py
```