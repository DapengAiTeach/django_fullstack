from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthSessionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="alice123456")

    def test_login_required_redirects_to_login_url(self):
        # 未登录访问 profile 应重定向到 LOGIN_URL，并携带 next
        resp = self.client.get(reverse("movies:profile"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp.url)
        self.assertIn("next=", resp.url)

    def test_login_flow_sets_session(self):
        # 登录成功后应跳转到 profile
        resp = self.client.post(reverse("accounts:login"), data={
            "username": "alice",
            "password": "alice123456",
        })
        self.assertEqual(resp.status_code, 302)

        # 再访问 profile 应成功
        resp2 = self.client.get(reverse("movies:profile"))
        self.assertEqual(resp2.status_code, 200)

    def test_logout_clears_login(self):
        self.client.login(username="alice", password="alice123456")
        resp = self.client.get(reverse("accounts:logout"))
        self.assertEqual(resp.status_code, 302)

        # 退出后访问 profile 다시重定向
        resp2 = self.client.get(reverse("movies:profile"))
        self.assertEqual(resp2.status_code, 302)