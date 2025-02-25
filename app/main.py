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
from router import currency
from typing import List

import models
from database import SessionLocal, engine, get_db, create_db_and_tables
from sqlalchemy.orm import Session
from hashing import Hash
import jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

###############################################################################
# app = FastAPI()
app = FastAPI(title ="ChatOffside API", version="0.1.0")

app.mount("/api", StaticFiles(directory="static", html=True), name="static")

#We define authorizations for middleware components
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://chatoffside.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#We use a callback to trigger the creation of the table if they don't exist yet
#When the API is starting
@app.on_event("startup")
def on_startup():
    print("Calling Created DB and Tables")
    create_db_and_tables()

###############################################################################
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Get database session
        async with SessionLocal() as session:
            # Find user by email
            user = session.query(models.User).filter(models.User.email == username).first()
            
            if not user:
                return False
                
            # Verify password
            if not Hash.verify(password, user.password):
                return False
                
            # Check if user has admin role (you should add an is_admin field to User model)
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

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        try:
            # Verify and decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            role = payload.get("role")
            
            # Ensure it's an admin token
            if not email or role != "admin":
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
                
            # Verify user still exists and is admin
            async with SessionLocal() as session:
                user = session.query(models.User).filter(models.User.email == email).first()
                if not user or not user.is_admin:
                    return RedirectResponse(request.url_for("admin:login"), status_code=302)
                    
        except jwt.PyJWTError:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
{{ ... }}

authentication_backend = AdminAuth(secret_key=SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

# admin = Admin(app, engine)

class UserAdmin(ModelView, model=models.User):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [models.User.id, models.User.name]

class PostAdmin(ModelView, model=models.Post):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [models.Post.id, models.Post.title, models.Post.body, models.Post.author_id, models.Post.author]

class PromptAdmin(ModelView, model=models.Prompt):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [models.Prompt.id, models.Prompt.title, models.Prompt.body, models.Prompt.author_id, models.Prompt.author]


admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
admin.add_view(PromptAdmin)
###############################################################################

@app.get('/')
def index():
    return 'ChatOffside API'


app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(prompt.router)
app.include_router(project.router)
app.include_router(profession.router)
app.include_router(user.router)
app.include_router(offsideai.router)
app.include_router(currency.router)

###############################################################################
