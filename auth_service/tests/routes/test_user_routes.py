import unittest
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.testclient import TestClient
from app.routes.user_routes import UserRoutes
from app.services.user_services import UserServices

client = TestClient(UserRoutes().routes)

class TestUserRoutes(unittest.TestCase):
    
    def setUp(self):
        self.user_services = UserServices()
        self.test_user = self.user_services.register({"name": "test_user8", "password": "test_password"}).to_dict()

    def tearDown(self):
        self.user_services.delete_user(self.test_user["name"])

    def test_register(self):
        user_data = {"name": "new_test_user8", "password": "new_test_password"}

        response = client.post('/api/users', json=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "new_test_user8")

        self.user_services.delete_user(user_data["name"])

    def test_register_validation_error(self):
        user_data = {"name": "new_test_user8"}
        with self.assertRaises(RequestValidationError):
            client.post('/api/users', json=user_data)
        self.user_services.delete_user(user_data["name"])

    def test_login(self):
        user_data = {"username": "test_user8", "password": "test_password"}

        response = client.post('/api/users/login', json=user_data)

        self.assertEqual(response.status_code, 200)

    def test_login_fail_with_incorrect_username_or_password(self):
        user_data1 = {"username": "test_user88", "password": "test_password"}
        user_data1 = {"username": "test_user8", "password": "test_passwordd"}

        with self.assertRaises(HTTPException):
            response1 = client.post('/api/users/login', json=user_data1)
            self.assertEqual(response1.status_code, 401)
        with self.assertRaises(HTTPException):
            response2 = client.post('/api/users/login', json=user_data1)
            self.assertEqual(response2.status_code, 401)

    def test_login_validation_error(self):
        user_data = {"username": "test_user8"}
        with self.assertRaises(RequestValidationError):
            client.post('/api/users', json=user_data)
    