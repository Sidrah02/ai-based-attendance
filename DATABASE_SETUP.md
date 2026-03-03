# Database Setup Guide

## Overview
This project uses **PostgreSQL** as the primary database with **SQLAlchemy ORM** for async operations. All tables are automatically created when the application starts.

## Prerequisites

### 1. PostgreSQL Installation
Install PostgreSQL on your system:

**macOS (Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

### 2. Verify Installation
```bash
psql --version
psql -U postgres -h localhost -c "SELECT version();"
```

## Database Setup Steps

### Step 1: Create the Database
```bash
psql -U postgres -h localhost -c "CREATE DATABASE attendance_db;"
```

### Step 2: Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/attendance_db
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=10080
PORT=8000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
EMAIL_FROM=your-email@gmail.com
```

### Step 4: Start the Application
```bash
python -m uvicorn main:app --reload --port 8000
```

The application will automatically:
- Connect to PostgreSQL
- Create all tables based on SQLAlchemy models
- Display `✅ PostgreSQL Connected` in the console

### Step 5: Seed Initial Data (Optional)
Run the initialization script to add sample admins and subjects:

```bash
python scripts/init_db.py
```

## Database Tables

The following tables are created automatically:

| Table | Purpose |
|-------|---------|
| `admins` | Store admin users with authentication |
| `students` | Store student records with contact info |
| `subjects` | Store course/subject information |
| `attendance_sessions` | Store attendance session metadata |
| `attendance` | Store individual attendance records |

## Verify Database Setup

### Check Tables via psql
```bash
psql -U postgres -h localhost -d attendance_db -c "\dt"
```

### Check Table Structure
```bash
psql -U postgres -h localhost -d attendance_db -c "\d students"
```

### Test via API
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "success": true,
  "message": "AI Attendance System API (PostgreSQL) is running."
}
```

## Troubleshooting

### Connection Error: "could not connect to server"
- Verify PostgreSQL is running: `brew services list` (macOS) or `sudo systemctl status postgresql` (Linux)
- Check `DATABASE_URL` in `.env` matches your PostgreSQL credentials
- Ensure the database exists: `psql -U postgres -l`

### Table Not Found Error
- Restart the application to trigger `Base.metadata.create_all()`
- Check application startup logs for `✅ PostgreSQL Connected`

### Permission Denied
- Verify your PostgreSQL user credentials in `DATABASE_URL`
- Ensure the user has CREATE privileges: `ALTER USER postgres CREATEDB;`

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres@localhost:5432/attendance_db` | PostgreSQL connection string |
| `JWT_SECRET` | `change_me` | Secret key for JWT token signing (change in production!) |
| `JWT_ALGORITHM` | `HS256` | Algorithm for JWT encoding |
| `JWT_EXPIRES_MINUTES` | `10080` | JWT token expiration (7 days) |
| `PORT` | `8000` | FastAPI server port |
| `SMTP_HOST` | `smtp.gmail.com` | Email service host |
| `SMTP_PORT` | `587` | Email service port |
| `SMTP_USER` | `` | Email account username |
| `SMTP_PASS` | `` | Email account password |
| `EMAIL_FROM` | `` | Sender email address |

## Running Migrations (Future Use)

When schema changes are needed, use Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "Add new column"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

For now, the project uses `Base.metadata.create_all()` on startup. Migrate to Alembic as the schema stabilizes.
