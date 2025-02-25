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