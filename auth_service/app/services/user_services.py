from fastapi import Depends
from models.user_models import User
from sqlalchemy.orm import Session
import database.database


class UserServices:

    def __init__(self):
        self.session = Session()

    def register(self, user_data: dict):
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
