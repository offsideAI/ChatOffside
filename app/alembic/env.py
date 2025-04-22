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
