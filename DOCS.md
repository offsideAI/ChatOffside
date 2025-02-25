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

### Structure
Routes are separated into the router directory
Database models are defined in models.py
Business logic is organized in the repository pattern
Authentication is handled through OAuth2
API documentation is auto-generated and available in OpenAPI format
The application appears to be a full-stack application with FastAPI handling the backend and SvelteKit for the frontend (though the frontend code might be in a separate repository since it's not visible in this structure).


### Login Request

#### Here's how to make the login request:

Using curl:

```
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your.email@example.com" \
  -d "password=your_password"
```

Using Postman:
Method: POST
URL: http://localhost:8000/login
Headers:
Content-Type: application/x-www-form-urlencoded
Body (x-www-form-urlencoded):
Key: username (this is actually your email)
Key: password
The response will be in JSON format:

```
{
    "access_token": "eyJhbGc...[rest of JWT token]",
    "token_type": "bearer"
}
```

Important notes:

The endpoint uses email as the username field
The token is a JWT token using HS256 algorithm
For subsequent authenticated requests, you'll need to include the token in the Authorization header:
CopyInsert
Authorization: Bearer eyJhbGc...[your token]
If the login fails, you'll get one of these error responses:

404 Not Found with "Invalid Credentials" if the email doesn't exist
404 Not Found with "Incorrect password" if the password is wrong

### Registration endpooint

Registration endpoint is implemented at /users/

The endpoint is a POST request to /users/ that accepts a JSON body with the following required fields (based on the UserCreate model):

name: User's name
email: User's email address
password: User's password (which will be hashed before storage)
Here's how to use it:

Using curl:

```
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "your_secure_password",
    "profession_id": null
  }'

```

Using Postman:
Method: POST
URL: http://localhost:8000/users/
Headers:
Content-Type: application/json
Body (raw JSON):


```
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "your_secure_password",
    "profession_id": null
}
```

The endpoint will:

Hash the password using bcrypt
Create a new user in the database
Return the created user information (excluding the password)
The response will be in JSON format and include the user's ID and other non-sensitive information.

Note that after registration, you'll need to use the /login endpoint with your email and password to get an access token for authenticated requests.