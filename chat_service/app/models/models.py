from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, class_mapper

from app.database.database import Base


room_members = Table('room_members', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('room_id', Integer, ForeignKey('rooms.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)

    rooms = relationship('Room', secondary=room_members, back_populates='users')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in class_mapper(self.__class__).mapped_table.c}

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    type = Column(String, nullable=False)

    users = relationship('User', secondary=room_members, back_populates='rooms')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=True)
    type = Column(String, nullable=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
