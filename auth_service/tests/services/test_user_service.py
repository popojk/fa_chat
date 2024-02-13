from fastapi import HTTPException

import unittest
from unittest.mock import MagicMock
from app.services.user_services import UserServices
from app.models.user_models import User
from app.tools.bcrypt import hash_pass

class TestUserServices(unittest.TestCase):
  def setUp(self):
    self.user_services = UserServices()

  def tearDown(self):
    pass

  def test_register(self):
    user_data = {"name": "testuser", "password": "123"}
    returned_user = self.user_services.register(user_data)

    self.assertIsInstance(returned_user, User)

  def test_login_invalid_credentials(self):
    self.user_services.get_db = MagicMock(return_value=None)
    with self.assertRaises(HTTPException):
      self.user_services.login('testuser', '123')


