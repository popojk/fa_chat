from fastapi import Depends, HTTPException, status
from models.user_models import User
from sqlalchemy.orm import Session
from database.database import SessionLocal

from tools.bcrypt import hash_pass, verify_pass


class UserServices:

    def __init__(self):
        self.db = SessionLocal()

    def register(self, user_data: dict):
        hash = hash_pass(user_data['password'])
        user_data['password'] = hash
        new_user = User(**user_data)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def login(self, username, password):
        user = self.db.query(User).filter(User.name == username).first()
        if not user or not verify_pass(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user
