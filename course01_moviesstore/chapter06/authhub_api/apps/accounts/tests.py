from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthFlowTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="alice", password="123456")

    def test_jwt_login_and_profile_should_work(self):
        # 1) jwt login
        r = self.client.post("/api/auth/jwt/login/", data={"username": "alice", "password": "123456"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        access = r.data["data"]["access"]

        # 2) profile with Bearer access
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        r = self.client.get("/api/profile/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        self.assertEqual(r.data["data"]["username"], "alice")

    def test_jwt_refresh_should_work(self):
        r = self.client.post("/api/auth/jwt/login/", data={"username": "alice", "password": "123456"}, format="json")
        refresh = r.data["data"]["refresh"]

        r = self.client.post("/api/auth/jwt/refresh/", data={"refresh": refresh}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        self.assertIn("access", r.data["data"])

    def test_token_login_and_profile_should_work(self):
        r = self.client.post("/api/auth/token/login/", data={"username": "alice", "password": "123456"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        token = r.data["data"]["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        r = self.client.get("/api/profile/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)

    def test_session_login_should_work(self):
        r = self.client.post("/api/auth/session/login/", data={"username": "alice", "password": "123456"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)

        # SessionAuthentication 依赖 cookie，APITestCase client 会保留 cookie
        r = self.client.get("/api/profile/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)