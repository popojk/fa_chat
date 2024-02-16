from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5433/fa_chat"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def db_session_decorator(func):
    def wrapper(*args, **kwargs):
        with get_db() as db_session:
            kwargs['db'] = db_session
            result = func(*args, **kwargs)
            return result
    return wrapper
