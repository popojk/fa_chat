import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user_models import User
from app.database.database import Base

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:password@localhost:5433/test_fa_chat')
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_user_creation(self):
        user = User(name='testuser6', password='password123')
        self.session.add(user)
        self.session.commit()

        queried_user = self.session.query(User).filter_by(name="testuser6").first()

        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.name, 'testuser6')
        self.assertEqual(queried_user.password, 'password123')

    def test_unique_name_constraint(self):
        user1 = User(name='unique_user', password='password123')
        user2 = User(name='unique_user', password='different_password')

        self.session.add(user1)
        self.session.add(user2)

        with self.assertRaises(Exception):
            self.session.commit()
