import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get database credentials
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "127.0.0.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "")

# Construct database URL
DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

print(f"Testing connection to: postgresql://{POSTGRES_USERNAME}:****@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DATABASE}")

try:
    # Create engine and test connection
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Successfully connected to the database!")
        # Test a simple query
        result = connection.execute("SELECT version();")
        version = result.fetchone()[0]
        print(f"PostgreSQL version: {version}")
except SQLAlchemyError as e:
    print(f"Error connecting to the database: {str(e)}")