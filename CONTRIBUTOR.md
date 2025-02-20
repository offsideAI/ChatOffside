# ChatOffside Contributor Guide

Welcome to the ChatOffside project! This guide will help you understand the project structure and how to contribute effectively.

## Project Overview

ChatOffside is a FastAPI-based web application that uses SQLModel for database operations. The project implements a RESTful API with user authentication, and manages various entities including posts, prompts, projects, and professions.

## Project Structure

```
app/
├── alembic/              # Database migration files
├── router/              # API route handlers
├── static/             # Static files (HTML, images)
├── __init__.py
├── accesstoken.py      # JWT token management
├── database.py         # Database configuration
├── hashing.py         # Password hashing utilities
├── main.py            # Application entry point
├── models.py          # SQLModel database models
├── oauth2.py          # OAuth2 authentication
└── requirements.txt    # Project dependencies
```

## Key Components

### 1. Database Models (`models.py`)

The application uses SQLModel (built on SQLAlchemy) with the following main models:

- `User`: Manages user accounts and relationships
- `Post`: Handles blog or content posts
- `Prompt`: Manages AI prompts
- `Project`: Handles project information
- `Profession`: Manages professional information
- Various relationship models (e.g., `UserProfessionLink`)

### 2. API Routes (`router/`)

Routes are organized by functionality:
- `authentication.py`: User authentication endpoints
- `post.py`: Post management endpoints
- `prompt.py`: Prompt management endpoints
- `project.py`: Project management endpoints
- `profession.py`: Profession management endpoints
- `user.py`: User management endpoints
- `offsideai.py`: AI-specific functionality

### 3. Authentication (`oauth2.py`, `accesstoken.py`)

- JWT-based authentication system
- Token creation and validation
- Protected route decorators

### 4. Database Configuration (`database.py`)

- SQLModel engine configuration
- Database session management
- Migration support using Alembic

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the `app` directory
   - Required variables:
     - `SECRET_KEY`: For JWT token encryption
     - `ALGORITHM`: JWT algorithm (e.g., "HS256")
     - `POSTGRES_USERNAME`: Database username
     - `POSTGRES_PASSWORD`: Database password
     - `POSTGRES_HOSTNAME`: Database host
     - `POSTGRES_PORT`: Database port
     - `POSTGRES_DATABASE`: Database name

4. Initialize the database:
   ```bash
   cd app
   alembic upgrade head
   ```

## Development Guidelines

### Code Style

1. Follow PEP 8 guidelines for Python code
2. Use type hints for function parameters and return values
3. Document functions and classes using docstrings
4. Keep functions focused and single-purpose

### Database Changes

1. Always use Alembic for database migrations
2. Create new migrations:
   ```bash
   alembic revision --autogenerate -m "description"
   ```
3. Apply migrations:
   ```bash
   alembic upgrade head
   ```

### API Development

1. Place new endpoints in appropriate router files
2. Use dependency injection for database sessions and authentication
3. Follow REST principles
4. Implement proper error handling
5. Document API endpoints using FastAPI's built-in documentation support

### Testing

1. Write unit tests for new features
2. Ensure existing tests pass before submitting PRs
3. Test database migrations both up and down

## Pull Request Process

1. Create a new branch for your feature/fix
2. Write clear, concise commit messages
3. Update documentation as needed
4. Ensure all tests pass
5. Submit PR with detailed description of changes

## API Documentation

The API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Admin Interface

The project includes an admin interface with:
- User management
- Post management
- Prompt management
- Protected by authentication

## Deployment

The application is configured to work with:
- PostgreSQL database
- CORS middleware for specified origins
- Static file serving

## Need Help?

- Check existing issues
- Review the FastAPI documentation
- Review the SQLModel documentation
- Create a new issue for bugs or feature requests

## License

Please review the project's LICENSE file for terms of use and distribution.
