# Local Development Setup Guide

This guide will help you set up and run the ChatOffside project locally.

## Prerequisites

1. Python 3.8 or higher
2. PostgreSQL database
3. pip (Python package manager)
4. Git

## Setup Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ChatOffside
```

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m myvenv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

1. Install PostgreSQL if you haven't already
2. Create a new database for the project:
```sql
CREATE DATABASE chatoffside;
```

### 5. Configure Environment Variables

Create a `.env` file in the `app` directory with the following variables:

```env
# JWT Configuration
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"

# Database Configuration
POSTGRES_USERNAME="your-postgres-username"
POSTGRES_PASSWORD="your-postgres-password"
POSTGRES_HOSTNAME="localhost"
POSTGRES_PORT=5432
POSTGRES_DATABASE="chatoffside"
```

### 6. Initialize the Database

Run the database migrations:

```bash
# Make sure you're in the app directory
cd app
alembic upgrade head
```

### 7. Run the Development Server

```bash
# Make sure you're in the app directory
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Testing the API

### 1. Access API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Create a Test User

You can create a test user using the API:

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Test User",
           "email": "test@example.com",
           "password": "testpassword123"
         }'
```

### 3. Get Authentication Token

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=testpassword123"
```

Save the returned access token for subsequent requests.

### 4. Test Protected Endpoints

Use the access token to test protected endpoints:

```bash
# Example: Create a new post
curl -X POST "http://localhost:8000/posts/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Test Post",
           "body": "This is a test post"
         }'
```

## Running Tests

The project uses Python's unittest framework. To run the tests:

```bash
# Make sure you're in the app directory
python -m pytest
```

## Common Issues and Solutions

### Database Connection Issues

1. Ensure PostgreSQL is running:
```bash
# On macOS
brew services list
# On Linux
sudo service postgresql status
```

2. Verify database credentials in `.env` file
3. Check if database exists:
```sql
psql -U postgres -l
```

### Migration Issues

If you encounter migration issues:

1. Reset migrations:
```bash
alembic downgrade base
alembic upgrade head
```

2. If problems persist, delete the migrations folder and reinitialize:
```bash
rm -rf alembic/versions/*
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### Server Won't Start

1. Check if port 8000 is already in use:
```bash
lsof -i :8000
```

2. Use a different port if needed:
```bash
uvicorn main:app --reload --port 8001
```

## Development Tools

### API Testing Tools
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- Built-in Swagger UI at `/docs`

### Database Tools
- [pgAdmin](https://www.pgadmin.org/) - PostgreSQL GUI
- [DBeaver](https://dbeaver.io/) - Universal Database Tool

## Debugging

1. Enable debug mode in FastAPI:
```python
app = FastAPI(debug=True)
```

2. Use logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. Use FastAPI's built-in debugger by raising HTTPException with detail:
```python
from fastapi import HTTPException
raise HTTPException(status_code=400, detail="Debug information here")
```

## Code Quality Tools

1. Install development dependencies:
```bash
pip install black flake8 mypy
```

2. Format code:
```bash
black .
```

3. Run linter:
```bash
flake8 .
```

4. Type checking:
```bash
mypy .
```
