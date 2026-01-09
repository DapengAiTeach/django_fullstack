from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginRequiredNextTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="alice123456")

    def test_redirect_to_login_with_next(self):
        # 未登录访问 VIP，应该 302 到 login 并携带 next
        resp = self.client.get(reverse("movies:vip"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp.url)
        self.assertIn("next=", resp.url)

    def test_login_then_redirect_back_to_next(self):
        # 模拟用户先访问 VIP -> 得到 next=/vip/
        vip_url = reverse("movies:vip")
        login_url = reverse("accounts:login") + f"?next={vip_url}"

        # 在带 next 的登录页面提交账号
        resp = self.client.post(login_url, data={
            "username": "alice",
            "password": "alice123456",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, vip_url)  # ✅ 登录后优先回 next

    def test_login_without_next_goes_to_default(self):
        # 不带 next 登录，应该去 LOGIN_REDIRECT_URL（我们设置为 vip）
        resp = self.client.post(reverse("accounts:login"), data={
            "username": "alice",
            "password": "alice123456",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse("movies:vip"))