# ChatOffside - Complete Bootstrap Guide

This document provides a step-by-step guide to recreate the ChatOffside project from scratch, following the exact development path taken to reach the current state on the `release` branch.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Initial Project Setup](#phase-1-initial-project-setup)
4. [Phase 2: Basic FastAPI Application](#phase-2-basic-fastapi-application)
5. [Phase 3: Database Models with SQLModel](#phase-3-database-models-with-sqlmodel)
6. [Phase 4: Authentication & JWT](#phase-4-authentication--jwt)
7. [Phase 5: Core API Endpoints](#phase-5-core-api-endpoints)
8. [Phase 6: Advanced Features](#phase-6-advanced-features)
9. [Phase 7: Database Migrations with Alembic](#phase-7-database-migrations-with-alembic)
10. [Phase 8: OpenAI Integration](#phase-8-openai-integration)
11. [Phase 9: Admin Panel](#phase-9-admin-panel)
12. [Phase 10: Production Readiness](#phase-10-production-readiness)
13. [Phase 11: Currency API Feature](#phase-11-currency-api-feature)
14. [Testing & Deployment](#testing--deployment)

---

## Project Overview

**ChatOffside** is a SKAP Stack (SvelteKit - FastAPI - Postgres) application designed as a chatbot for prompt management and project management. It integrates with OpenAI's GPT models to provide AI-powered features including vision analysis, document processing, and text generation.

**Core Technologies:**
- FastAPI (Python web framework)
- SQLModel/SQLAlchemy (ORM)
- PostgreSQL (Production database)
- SQLite (Development database)
- Alembic (Database migrations)
- JWT Authentication (python-jose, passlib)
- SQLAdmin (Admin interface)
- OpenAI API
- Docker (Deployment)

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.9 or higher** (tested with Python 3.10.9)
- **PostgreSQL** (for production, optional for development)
- **Git**
- **pip** (Python package manager)
- **OpenSSL** (for generating secret keys)
- **Docker** (optional, for deployment)
- **Node.js & npm** (for frontend, if developing the full stack)

Verify installations:
```bash
python --version  # Should be 3.9+
pip --version
git --version
psql --version  # Optional for development
```

---

## Phase 1: Initial Project Setup

### Step 1.1: Create Project Directory

```bash
# Create project root directory
mkdir ChatOffside
cd ChatOffside

# Initialize git repository
git init

# Create README.md
cat > README.md << 'EOF'
# ChatOffside
ChatOffside is a chatbot for prompt management and project management
ChatOffside is a SKAP Stack (SvelteKit - (fast)API - Postgres- stack) toolkit for building, testing and deploying fullstack AI plugins and applications

This project uses FastAPI and SQLModel
EOF

git add README.md
git commit -m "Initial commit"
```

### Step 1.2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv myvenv

# Activate virtual environment
# On macOS/Linux:
source myvenv/bin/activate

# On Windows:
# myvenv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 1.3: Create Application Directory

```bash
# Create app directory structure
mkdir -p app
mkdir -p app/router
mkdir -p app/repository
mkdir -p app/static
mkdir -p app/alembic

# Create __init__.py files
touch app/__init__.py
touch app/router/__init__.py
```

### Step 1.4: Install Core Dependencies

```bash
# Install FastAPI and Uvicorn
pip install fastapi
pip install "uvicorn[standard]"
pip install pydantic

# Verify versions
python --version  # Should show Python 3.10.9 or higher
uvicorn --version  # Should show uvicorn with CPython
```

---

## Phase 2: Basic FastAPI Application

### Step 2.1: Create Basic Main Application

Create `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="ChatOffside API", version="0.1.0")

@app.get('/')
def index():
    return 'ChatOffside API'
```

### Step 2.2: Test the Application

```bash
# Navigate to app directory
cd app

# Run the development server
uvicorn main:app --reload
```

Visit `http://localhost:8000` and `http://localhost:8000/docs` to verify the application is running.

### Step 2.3: Add Static Files Support

Update `app/main.py` to serve static files:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ChatOffside API", version="0.1.0")

# Mount static files
app.mount("/api", StaticFiles(directory="static", html=True), name="static")

@app.get('/')
def index():
    return 'ChatOffside API'
```

### Step 2.4: Configure CORS Middleware

Add CORS support to `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ChatOffside API", version="0.1.0")

app.mount("/api", StaticFiles(directory="static", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://chatoffside.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return 'ChatOffside API'
```

---

## Phase 3: Database Models with SQLModel

### Step 3.1: Install Database Dependencies

```bash
pip install sqlalchemy
pip install sqlmodel
pip install psycopg2-binary  # For PostgreSQL
```

### Step 3.2: Create Environment Configuration

Create `app/.env`:

```bash
# Generate a secret key
openssl rand -base64 32
```

Create `app/.env` file:

```env
# JWT Configuration
SECRET_KEY="your-generated-secret-key-here"
ALGORITHM="HS256"

# Database Configuration - Development
ENV="development"

# Database Configuration - Production (optional for now)
POSTGRES_USERNAME="your-postgres-username"
POSTGRES_PASSWORD="your-postgres-password"
POSTGRES_HOSTNAME="127.0.0.1"
POSTGRES_PORT=5432
POSTGRES_DATABASE="chatoffside_dev_1"

# OpenAI API Key (will be added later)
# OPENAI_API_KEY="your-openai-api-key"
```

Install python-dotenv:

```bash
pip install python-dotenv
```

### Step 3.3: Create Database Configuration

Create `app/database.py`:

```python
import os, sys
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Determine environment (default to 'development' if not set)
ENV = os.environ.get("ENV", "development")
logger.info(f"Current environment: {ENV}")

if ENV == "development":
    # Use SQLite for local development
    SQLALCHEMY_SQLITE_URL = "sqlite:///./blog.db"
    logger.info(f"Using SQLite database at: {SQLALCHEMY_SQLITE_URL}")
    # Create engine with SQLite-specific arguments
    engine = create_engine(
        SQLALCHEMY_SQLITE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Use PostgreSQL for production
    POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
    POSTGRES_PASSWORD = "****"  # Mask password in logs
    POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "127.0.0.1")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "")

    logger.info(f"Using PostgreSQL database at: postgresql://{POSTGRES_USERNAME}:****@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DATABASE}")

    # Actual connection URL with real password
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{os.environ.get('POSTGRES_PASSWORD')}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

def create_db_and_tables():
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

def get_session():
    with Session(engine) as session:
        yield session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 3.4: Create Data Models

Create `app/models.py`:

```python
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from typing import List, Optional, Union, ForwardRef
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

###############################################################################
# UserProfessionLink - Many-to-Many relationship table

class UserProfessionLink(SQLModel, table=True):
    profession_id: Optional[int] = Field(
        default=None, foreign_key="profession.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )

###############################################################################
# Profession Model

class ProfessionBase(SQLModel):
    title: str
    description: str = Field(sa_column=Column(TEXT))


class Profession(ProfessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="professions", link_model=UserProfessionLink)

###############################################################################
# User Model

class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str
    password: str
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")
    is_admin: bool = Field(default=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="author")
    prompts: List["Prompt"] = Relationship(back_populates="author")
    projects: List["Project"] = Relationship(back_populates="author")
    professions: List["Profession"] = Relationship(back_populates="users", link_model=UserProfessionLink)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

###############################################################################
# Profession (extended schemas)

class ProfessionCreate(ProfessionBase):
    users: Optional[List["User"]] = None

class ProfessionRead(ProfessionBase):
    id: Optional[str] = None
    users: Optional[List["User"]] = None

class ProfessionUpdate(SQLModel):
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    users: Optional[List["User"]] = None

class ProfessionReadWithUser(ProfessionRead):
    users: Optional[List["User"]] = None

class UserReadWithProfessions(UserRead):
    professions: List[ProfessionRead] = []

###############################################################################
# Post Model

class PostBase(SQLModel):
    title: str
    body: str
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: Optional[User] = Relationship(back_populates="posts")

class PostRead(PostBase):
    id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(SQLModel):
    id: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[int] = None

class PostReadWithUser(PostRead):
    author: Optional[UserRead] = None

class UserReadWithPosts(UserRead):
    posts: List[PostRead] = []
    prompts: List[PostRead] = []

###############################################################################
# Prompt Model

class PromptBase(SQLModel):
    title: str
    body: str = Field(sa_column=Column(TEXT))
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Prompt(PromptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: Optional[User] = Relationship(back_populates="prompts")

class PromptRead(PromptBase):
    id: Optional[int] = None

class PromptCreate(PromptBase):
    pass

class PromptUpdate(SQLModel):
    id: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[int] = None

class PromptReadWithUser(PromptRead):
    author: Optional[UserRead] = None

class UserReadWithPrompts(UserRead):
    prompts: List[PromptRead] = []

###############################################################################
# Project Model

class ProjectBase(SQLModel):
    title: str
    body: str = Field(sa_column=Column(TEXT))
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: Optional[User] = Relationship(back_populates="projects")

class ProjectRead(ProjectBase):
    id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(SQLModel):
    id: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[int] = None

class ProjectReadWithUser(ProjectRead):
    author: Optional[UserRead] = None

class UserReadWithProjects(UserRead):
    projects: List[ProjectRead] = []

###############################################################################
# Auth Models

class Login(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    email: str | None = None

###############################################################################
```

### Step 3.5: Update Main Application with Database

Update `app/main.py` to initialize database on startup:

```python
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import models
from database import create_db_and_tables

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FastAPI(title="ChatOffside API", version="0.1.0")

app.mount("/api", StaticFiles(directory="static", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://chatoffside.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    if os.environ.get("ENV") == "development":
        print("Development environment: Creating DB and Tables")
        create_db_and_tables()
    else:
        print("Production environment: Skipping automatic table creation")

@app.get('/')
def index():
    return 'ChatOffside API'
```

---

## Phase 4: Authentication & JWT

### Step 4.1: Install Authentication Dependencies

```bash
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install bcrypt
pip install python-multipart
```

### Step 4.2: Create Password Hashing Module

Create `app/hashing.py`:

```python
from passlib.context import CryptContext

pwdCtx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        hashedPassword = pwdCtx.hash(password)
        return hashedPassword

    def verify(plain_password, hashed_password):
        return pwdCtx.verify(plain_password, hashed_password)
```

### Step 4.3: Create JWT Token Module

Create `app/accesstoken.py`:

```python
import os, sys
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
import models

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = models.TokenData(email=email)
    except JWTError:
        raise credentials_exception
```

### Step 4.4: Create OAuth2 Module

Create `app/oauth2.py`:

```python
import os, sys
from os.path import join, dirname
from dotenv import load_dotenv
from http.client import HTTPException
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session
import accesstoken
from database import get_db
import models

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], request: Request, session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = session.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise credentials_exception

    return user
```

### Step 4.5: Create Authentication Router

Create `app/router/authentication.py`:

```python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

import models, database
from hashing import Hash
from sqlalchemy.orm import Session
import accesstoken

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    # generate jwt token and return
    access_token = accesstoken.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## Phase 5: Core API Endpoints

### Step 5.1: Create User Router

Create `app/router/user.py`:

```python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

import database, models
from sqlalchemy.orm import Session
from hashing import Hash

router = APIRouter(
    tags=['Users']
)

###############################################################################
# User Endpoints

@router.post('/users/', response_model=models.UserRead)
def create_user(
    *,
    session: Session = Depends(database.get_session),
    user: models.UserCreate
):
    # Hash the password
    hashed_password = Hash.bcrypt(user.password)

    # Create a new User instance with the hashed password
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get('/users/', response_model=List[models.UserRead])
def read_users(
    *,
    session: Session = Depends(database.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    users = session.exec(select(models.User).offset(offset).limit(limit)).all()
    return users

@router.get('/users/{user_id}', response_model=models.UserReadWithPosts)
def read_user(
    *,
    user_id:int,
    session: Session = Depends(database.get_session)
):
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


@router.patch('/users/{user_id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(
    *,
    session: Session = Depends(database.get_session),
    user_id: int,
    user: models.UserUpdate,
):
    db_user = session.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        if key == 'password':  # Hash the password if it's being updated
            value = Hash.bcrypt(value)
        setattr(db_user, key, value)

    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete('/users/{user_id}')
def delete_user(
    *,
    session: Session = Depends(database.get_session),
    user_id: int
):
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
```

### Step 5.2: Create Post Router

Create `app/router/post.py`:

```python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query
import database, models
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import oauth2

router = APIRouter(
    tags=['Posts']
)

###############################################################################
# Post Endpoints

@router.post('/posts/', response_model=models.PostRead)
def create_post(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    post: models.PostCreate
):
    db_post = models.Post.from_orm(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return post

@router.get('/posts', response_model=List[models.PostRead])
def read_posts(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    posts = session.query(models.Post).filter(models.Post.author_id == current_user.id).offset(offset).limit(limit).all()
    return posts

@router.get('/posts/{post_id}', response_model=models.PostReadWithUser)
def read_post(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    post_id: int
):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} is not available")
    return post

@router.patch('/posts/{post_id}', response_model=models.PostRead)
def update_post(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    post_id: int,
    post: models.PostUpdate
):
    db_post = session.get(models.Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    post_data = post.dict(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.delete('/posts/{post_id}')
def delete_post(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    post_id: int,
):
    post = session.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    session.delete(post)
    session.commit()
    return {'detail': f"Post with id {post_id} was deleted"}
```

### Step 5.3: Create Prompt Router

Create `app/router/prompt.py`:

```python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query
import database, models
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import oauth2

router = APIRouter(
    tags=['Prompts']
)

###############################################################################
# Prompt Endpoints

@router.post('/prompts/', response_model=models.PromptRead)
def create_prompt(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    prompt: models.PromptCreate
):
    db_prompt = models.Prompt.from_orm(prompt)
    session.add(db_prompt)
    session.commit()
    session.refresh(db_prompt)
    return prompt

@router.get('/prompts', response_model=List[models.PromptRead])
def read_prompts(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    prompts = session.query(models.Prompt).filter(models.Prompt.author_id == current_user.id).offset(offset).limit(limit).all()
    return prompts

@router.get('/prompts/{prompt_id}', response_model=models.PromptReadWithUser)
def read_prompt(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    prompt_id: int
):
    prompt = session.get(models.Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with id {prompt_id} is not available")
    return prompt

@router.patch('/prompts/{prompt_id}', response_model=models.PromptRead)
def update_prompt(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    prompt_id: int,
    prompt: models.PromptUpdate
):
    db_prompt = session.get(models.Prompt, prompt_id)
    if not db_prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with id {prompt_id} not found")
    prompt_data = prompt.dict(exclude_unset=True)
    for key, value in prompt_data.items():
        setattr(db_prompt, key, value)
    session.add(db_prompt)
    session.commit()
    session.refresh(db_prompt)
    return db_prompt

@router.delete('/prompts/{prompt_id}')
def delete_prompt(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    prompt_id: int,
):
    prompt = session.get(models.Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with id {prompt_id} not found")
    session.delete(prompt)
    session.commit()
    return {'detail': f"Prompt with id {prompt_id} was deleted"}
```

### Step 5.4: Create Project Router

Create `app/router/project.py` (similar structure to prompt.py, replace "Prompt" with "Project")

### Step 5.5: Create Profession Router

Create `app/router/profession.py` (similar structure to prompt.py, replace "Prompt" with "Profession")

### Step 5.6: Update Main Application to Include Routers

Update `app/main.py`:

```python
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from router import post
from router import prompt
from router import project
from router import profession
from router import user
from router import authentication

import models
from database import create_db_and_tables

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FastAPI(title="ChatOffside API", version="0.1.0")

app.mount("/api", StaticFiles(directory="static", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://chatoffside.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    if os.environ.get("ENV") == "development":
        print("Development environment: Creating DB and Tables")
        create_db_and_tables()
    else:
        print("Production environment: Skipping automatic table creation")

@app.get('/')
def index():
    return 'ChatOffside API'

# Include routers
app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(prompt.router)
app.include_router(project.router)
app.include_router(profession.router)
app.include_router(user.router)
```

---

## Phase 6: Advanced Features

### Step 6.1: Create Static Files for ChatGPT Plugin

Create `app/static/ai-plugin.json`:

```json
{
    "schema_version": "v1",
    "name_for_human": "ChatOffside",
    "name_for_model": "ChatOffside",
    "description_for_human": "ChatOffside Project Management.",
    "description_for_model": "Chatbot plugin for project management.",
    "logo_url": "offsideai_400x400.jpg",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "https://chatoffside.onrender.com/openapi.json",
        "is_user_authenticated": false
    },
    "legal_info_url": "http://offside.ai",
    "contact_email": "info@offside.ai"
}
```

Create `app/static/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatOffside API</title>
</head>
<body>
    <h1>Welcome to ChatOffside API</h1>
    <p>A chatbot for prompt management and project management</p>
    <ul>
        <li><a href="/docs">API Documentation</a></li>
        <li><a href="/redoc">ReDoc Documentation</a></li>
    </ul>
</body>
</html>
```

Add a logo image to `app/static/offsideai_400x400.jpg` (your logo file).

---

## Phase 7: Database Migrations with Alembic

### Step 7.1: Install Alembic

```bash
pip install alembic
```

### Step 7.2: Initialize Alembic

```bash
cd app
alembic init alembic
```

This creates:
- `alembic/` directory
- `alembic.ini` configuration file

### Step 7.3: Configure Alembic

Edit `app/alembic/script.py.mako` and add the SQLModel import:

```python
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # Add this line
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
```

### Step 7.4: Configure Alembic env.py

Edit `app/alembic/env.py`:

```python
from logging.config import fileConfig
from models import *
from sqlmodel import SQLModel

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os, sys
from os.path import join, dirname
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# Determine environment (default to 'development' if not set)
ENV = os.environ.get("ENV", "development")
logger.info(f"Alembic running in environment: {ENV}")

if ENV == "development":
    # Use SQLite for local development
    SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
    logger.info(f"Using SQLite database at: {SQLALCHEMY_DATABASE_URL}")
else:
    # Use PostgreSQL for production
    POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "127.0.0.1")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    logger.info(f"Using PostgreSQL database at: postgresql://{POSTGRES_USERNAME}:****@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DATABASE}")

config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    if ENV == "development":
        # For SQLite
        configuration = {
            "sqlalchemy.url": SQLALCHEMY_DATABASE_URL
        }
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            connect_args={"check_same_thread": False}
        )
    else:
        # For PostgreSQL
        configuration = {
            "sqlalchemy.url": SQLALCHEMY_DATABASE_URL
        }
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Step 7.5: Create Initial Migration

```bash
cd app
alembic revision --autogenerate -m "initial"
```

### Step 7.6: Run Migrations

```bash
cd app
alembic upgrade head
```

---

## Phase 8: OpenAI Integration

### Step 8.1: Install OpenAI

```bash
pip install openai
```

### Step 8.2: Add OpenAI API Key to .env

Update `app/.env`:

```env
# OpenAI API Key
OPENAI_API_KEY="your-openai-api-key-here"
```

### Step 8.3: Create OffsideAI Router

Create `app/router/offsideai.py`:

```python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, UploadFile, File
import database, models
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import oauth2
import openai
import base64
import re

router = APIRouter(
    tags=['offsidei']
)

###############################################################################
# OpenAI Endpoints

@router.get('/offsideai/jsonfunctioncalling')
def dojsonfunctioncalling(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    query: str = Query(..., description="The content to send to the OpenAI model")
):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = [
            {
                "role": "system",
                "content": "Generate JSON response"
            },
            {
                "role": "user",
                "content": query

            }
        ],
        response_format={ "type": "json_object" }
    )
    return response.choices[0].message.content

@router.get('/offsideai/functioncalling')
def dofunctioncalling(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    query: str = Query(..., description="The content to send to the OffsideAI model")
):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = [
            {
                "role": "system",
                "content": "Generate regular response"
            },
            {
                "role": "user",
                "content": query

            }
        ]
    )
    return response.choices[0].message.content

@router.get('/offsideai/urlvision')
async def dourlvisionmagic(
    *,
    imageurl: str = Query(..., description="The url of the file")
):
    client = openai.OpenAI()

    query: str = "What's in this image?"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        }
                    }
                ]
            }
        ],
        max_tokens = 300
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    print(response_string)
    return response_string

@router.get('/offsideai/docvision')
async def dodocumentmagic(
    *,
    imageurl: str = Query(..., description="The url of the file")
):
    client = openai.OpenAI()

    query: str = "Can you take the contents of this image and explain all the details and also interpret and summarize the information and suggest steps?"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        }
                    }
                ]
            }
        ],
        max_tokens = 400
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    response_string = replace_patterns(response_string)
    print(response_string)
    return response_string

@router.get('/offsideai/visioncounter')
async def dovisioncountermagic(
    *,
    imageurl: str = Query(..., description="The url of the file")
):
    client = openai.OpenAI()

    query: str = "Can you take the contents of this image and count the number of items in the image? Just return the number and the item name"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        }
                    }
                ]
            }
        ],
        max_tokens = 400
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    response_string = replace_patterns(response_string)
    print(response_string)
    return response_string

@router.get('/offsideai/visionhashtags')
async def dovisionhashtagsmagic(
    *,
    imageurl: str = Query(..., description="The url of the file")
):
    client = openai.OpenAI()

    query: str = "Can you take the contents of this image and generate a list of 15 relevant hashtags. Focus on capturing the key themes and elements present in the image. Ensure the hashtags are suitable for use on social media platforms like Instagram and Twitter, emphasizing salient items in the image. Present the hashtags in a clear, space-seperated list, with no numbering. "
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        }
                    }
                ]
            }
        ],
        max_tokens = 400
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    response_string = replace_patterns(response_string)
    print(response_string)
    return response_string

def replace_patterns(text):
    # Pattern for **<string>**
    pattern1 = r"\*\*<([^>]*)>\*\*"
    replacement1 = r"<\1> Section"

    # Pattern for ###
    pattern2 = r"###"
    replacement2 = "..."

    # Perform replacements
    text = re.sub(pattern1, replacement1, text)
    text = re.sub(pattern2, replacement2, text)

    return text
```

### Step 8.4: Update Main to Include OffsideAI Router

Update `app/main.py` to include the offsideai router:

```python
from router import offsideai

# ... other code ...

app.include_router(offsideai.router)
```

---

## Phase 9: Admin Panel

### Step 9.1: Install SQLAdmin

```bash
pip install sqladmin
```

### Step 9.2: Add Admin Panel to Main Application

Update `app/main.py` to include admin panel:

```python
import os, sys
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Response, status, HTTPException
from typing import Optional
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from router import post
from router import prompt
from router import project
from router import profession
from router import user
from router import authentication
from router import offsideai

import models
from database import SessionLocal, engine, get_db, create_db_and_tables
from sqlalchemy.orm import Session
from hashing import Hash
import jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

app = FastAPI(title="ChatOffside API", version="0.1.0")

app.mount("/api", StaticFiles(directory="static", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://chatoffside.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    if os.environ.get("ENV") == "development":
        print("Development environment: Creating DB and Tables")
        create_db_and_tables()
    else:
        print("Production environment: Skipping automatic table creation")

###############################################################################
# Admin Panel Setup

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Get database session
        db = SessionLocal()
        try:
            # Find user by email
            user = db.query(models.User).filter(models.User.email == username).first()

            if not user:
                return False

            # Verify password
            if not Hash.verify(password, user.password):
                return False

            # Check if user has admin role
            if not user.is_admin:
                return False

            # Generate JWT token
            access_token = jwt.encode({
                "sub": user.email,
                "role": "admin",
                "exp": datetime.utcnow() + timedelta(minutes=30)
            }, SECRET_KEY, algorithm=ALGORITHM)

            # Store token in session
            request.session.update({"token": access_token})
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("role") != "admin":
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
            return None
        except (JWTError, Exception):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

authentication_backend = AdminAuth(secret_key=SECRET_KEY)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
    base_url="/admin"
)

# Admin views
class UserAdmin(ModelView, model=models.User):
    column_list = [models.User.id, models.User.name, models.User.email, models.User.is_admin]
    column_searchable_list = [models.User.name, models.User.email]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class PostAdmin(ModelView, model=models.Post):
    column_list = [models.Post.id, models.Post.title, models.Post.author_id]
    column_searchable_list = [models.Post.title]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class PromptAdmin(ModelView, model=models.Prompt):
    column_list = [models.Prompt.id, models.Prompt.title, models.Prompt.author_id]
    column_searchable_list = [models.Prompt.title]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class ProjectAdmin(ModelView, model=models.Project):
    column_list = [models.Project.id, models.Project.title, models.Project.author_id]
    column_searchable_list = [models.Project.title]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

# Register admin views
admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
admin.add_view(PromptAdmin)
admin.add_view(ProjectAdmin)

###############################################################################

@app.get('/')
def index():
    return 'ChatOffside API'

# Include routers
app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(prompt.router)
app.include_router(project.router)
app.include_router(profession.router)
app.include_router(user.router)
app.include_router(offsideai.router)
```

### Step 9.3: Create Admin User Script

Create `app/create_admin.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from hashing import Hash
from dotenv import load_dotenv
import os
from os.path import join, dirname

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Create database connection
engine = create_engine("sqlite:///./blog.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_admin():
    with SessionLocal() as db:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_admin:
            print("Admin user already exists!")
            return

        admin_user = User(
            name="Admin User",
            email="admin@example.com",
            password=Hash.bcrypt("your-secure-password"),
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")

if __name__ == "__main__":
    create_admin()
```

Run the script to create an admin user:

```bash
cd app
python create_admin.py
```

---

## Phase 10: Production Readiness

### Step 10.1: Create Requirements File

Generate requirements.txt:

```bash
cd app
pip freeze > requirements.txt
```

The `requirements.txt` should include (verify versions match):

```
alembic==1.10.2
fastapi==0.95.0
uvicorn==0.21.1
sqlalchemy==1.4.41
sqlmodel==0.0.8
psycopg2-binary==2.9.5
python-dotenv==1.0.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.0.1
python-multipart==0.0.6
sqladmin==0.10.1
openai==1.2.2
# ... and other dependencies
```

### Step 10.2: Create Documentation Files

Create `SETUP.md`:

```markdown
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
python -m venv myvenv

# Activate the virtual environment
# On macOS/Linux:
source myvenv/bin/activate
# On Windows:
.\myvenv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `app` directory with the following variables:

```env
# JWT Configuration
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"

# Database Configuration
ENV="development"

# For PostgreSQL (production)
POSTGRES_USERNAME="your-postgres-username"
POSTGRES_PASSWORD="your-postgres-password"
POSTGRES_HOSTNAME="localhost"
POSTGRES_PORT=5432
POSTGRES_DATABASE="chatoffside"

# OpenAI API
OPENAI_API_KEY="your-openai-api-key"
```

### 5. Initialize the Database

Run the database migrations:

```bash
cd app
alembic upgrade head
```

### 6. Run the Development Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 7. Access Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Admin Panel: `http://localhost:8000/admin`
```

Create `GETSTARTED.md` with quick start instructions.

Create `DEVELOPER.md` with developer guidelines.

Create `DOCS.md` with API endpoint documentation.

Create `MIGRATIONS.md` with Alembic migration instructions.

### Step 10.3: Create .gitignore

Create `.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
myvenv/
venv/
ENV/
env/

# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Alembic
alembic/versions/__pycache__/

# Logs
*.log
```

### Step 10.4: Create Dockerfile

Create `Dockerfile` in the root directory:

```dockerfile
FROM python:3.9

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
```

---

## Phase 11: Currency API Feature

### Step 11.1: Create Currency Router

Create `app/router/currency.py`:

```python
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

def load_currency_data():
    """
    Load currency data from the JSON file
    Returns the currency data as a dictionary
    """
    try:
        current_dir = Path(__file__).parent
        json_path = current_dir / 'currency.json'
        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Currency data file not found"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Error parsing currency data file"
        )

@router.get("/currencyapi/latest")
async def get_latest_rates():
    """
    Get the latest currency exchange rates
    Returns a dictionary with meta information and currency rates
    """
    return load_currency_data()
```

### Step 11.2: Create Currency Data File

Create `app/router/currency.json`:

```json
{
    "meta": {
        "last_updated_at": "2025-02-20T23:59:59Z"
    },
    "data": {
        "AUD": 1.5345,
        "BGN": 1.8123,
        "BRL": 5.1234,
        "CAD": 1.3567,
        "CHF": 0.8912,
        "CNY": 7.2345,
        "CZK": 22.456,
        "DKK": 6.8901,
        "EUR": 0.9234,
        "GBP": 0.7890,
        "HKD": 7.8123,
        "HUF": 345.67,
        "IDR": 15678.9,
        "ILS": 3.6789,
        "INR": 82.345,
        "ISK": 134.56,
        "JPY": 149.23,
        "KRW": 1312.34,
        "MXN": 17.234,
        "MYR": 4.5678,
        "NOK": 10.567,
        "NZD": 1.6234,
        "PHP": 55.678,
        "PLN": 4.0123,
        "RON": 4.5678,
        "SEK": 10.234,
        "SGD": 1.3456,
        "THB": 35.678,
        "TRY": 30.123,
        "USD": 1.0,
        "ZAR": 18.234
    }
}
```

### Step 11.3: Update Main to Include Currency Router

Update `app/main.py`:

```python
from router import currency

# ... other code ...

app.include_router(currency.router)
```

---

## Testing & Deployment

### Testing the API

1. **Test User Registration**:

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

2. **Test Login**:

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

3. **Test Protected Endpoints**:

```bash
# Get access token from login, then:
curl -X GET "http://localhost:8000/posts" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

4. **Test OpenAI Integration**:

```bash
curl -X GET "http://localhost:8000/offsideai/functioncalling?query=Hello" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

5. **Test Currency API**:

```bash
curl -X GET "http://localhost:8000/currencyapi/latest"
```

### Deployment to Render/Heroku

1. **Set environment variables** in your hosting platform:
   - `ENV=production`
   - `SECRET_KEY`
   - `ALGORITHM`
   - Database credentials
   - `OPENAI_API_KEY`

2. **Run migrations** in production:

```bash
alembic upgrade head
```

3. **Start command** for production:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

### Docker Deployment

Build and run Docker container:

```bash
# Build image
docker build -t chatoffside:0.1.0 .

# Run container
docker run -p 10000:10000 --name chatoffside chatoffside:0.1.0
```

---

## Summary of Key Commits

Based on git history, here's the evolution timeline:

1. **Initial commit** (April 2023) - Basic project structure
2. **Added scaffold** - FastAPI basic setup
3. **Added User and Post models** - Basic database models
4. **Added Profession model** - Many-to-many relationship
5. **Improved README** - Documentation
6. **Added JWT authentication** - User authentication
7. **Added OpenAI integration** (November 2023) - AI features
8. **Added vision endpoints** - GPT-4 Vision integration
9. **Added document vision** - Document processing
10. **Added admin panel** - SQLAdmin integration
11. **Currency API** (February 2025) - Currency exchange rates
12. **Production hardening** (February 2025) - Security & environment separation
13. **Updated to GPT-4o** (April 2025) - Latest OpenAI model

---

## Conclusion

You have now recreated the ChatOffside project from scratch, following the exact development path taken. The application includes:

- ✅ FastAPI backend with JWT authentication
- ✅ SQLModel/SQLAlchemy ORM with PostgreSQL/SQLite support
- ✅ Alembic database migrations
- ✅ User, Post, Prompt, Project, and Profession models
- ✅ OpenAI GPT-4o integration with vision capabilities
- ✅ Admin panel with SQLAdmin
- ✅ Currency API
- ✅ Environment-based configuration (dev/prod)
- ✅ Docker deployment support
- ✅ Comprehensive API documentation

The project is production-ready and can be deployed to any hosting platform that supports Python/FastAPI applications.

