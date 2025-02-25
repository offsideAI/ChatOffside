#Docs
ChatOffside is a chatbot and project management application built using the SKAP Stack (SvelteKit - FastAPI - Postgres). Here's the project structure breakdown:

## Root Directory:
Multiple documentation files:
README.md: Main project documentation
DEVELOPER.md: Developer guidelines
SETUP.md: Setup instructions
GETSTARTED.md: Getting started guide
CONTRIBUTOR.md: Contribution guidelines

## Main Application (/app/):
### Core Files:
main.py: The FastAPI application entry point
database.py: Database configuration and connection setup
models.py: SQLAlchemy/SQLModel data models
oauth2.py: Authentication and authorization implementation
hashing.py: Password hashing utilities
### API Structure:
/router/: Contains API route definitions (including currency.py)
/repository/: Data access layer implementations
openapi.yaml: API documentation/specification
### Database:
Uses PostgreSQL (indicated by SKAP stack)
alembic/: Database migration tool and its configurations
alembic.ini: Alembic configuration file
blog.db: SQLite database (likely for development)
### Configuration:
.env: Environment variables (contains sensitive data)
.env.sample: Template for environment variables
requirements.txt: Python dependencies
### Static Assets:
/static/: Directory for static files
## Development Environment:
myvenv/: Python virtual environment directory
.vscode/: VS Code configuration
.gitignore: Git ignore rules
The project follows a typical FastAPI application structure with clear separation of concerns:

Routes are separated into the router directory
Database models are defined in models.py
Business logic is organized in the repository pattern
Authentication is handled through OAuth2
API documentation is auto-generated and available in OpenAPI format
The application appears to be a full-stack application with FastAPI handling the backend and SvelteKit for the frontend (though the frontend code might be in a separate repository since it's not visible in this structure).