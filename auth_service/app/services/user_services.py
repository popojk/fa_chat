from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user_models import User
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.database.database import get_db, db_session_decorator
from app.tools.bcrypt import hash_pass, verify_pass
from jose import JWTError, jwt

from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class UserServices:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    def __init__(self):
        # self.db = SessionLocal()
        pass

    @db_session_decorator
    def register(self, user_data: dict, db=None):
        try:
            user = db.query(User).filter(User.name == user_data['name']).first()
            if user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User {user_data["name"]} already exists'
                )
            hash = hash_pass(user_data['password'])
            user_data['password'] = hash
            new_user = User(**user_data)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            print(e)

    @db_session_decorator
    def login(self, username, password, db=None):
        user = db.query(User).filter(User.name == username).first()
        if not user or not verify_pass(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        user_dict = user.to_dict()
        del user_dict['password']
        jwt = self.create_access_token(user_dict)
        return jwt

    def create_access_token(self, data: dict, expires_delta: int = None):
        """create jwt token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=int(self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    @db_session_decorator
    def authenticate(self, token: str, db=None):
        try:
            payload = jwt.decode(token, self.SECRET_KEY,
                               algorithms=self.ALGORITHM)
            name: str = payload['name']
            if name is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return db.query(User).filter(User.name == name).first()

    @db_session_decorator
    def delete_user(self, name: str, db=None):
        stmt = delete(User).where(User.name == name)
        db.execute(stmt)
        db.commit()
