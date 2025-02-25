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
