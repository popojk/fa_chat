from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, class_mapper

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in class_mapper(self.__class__).mapped_table.c}
