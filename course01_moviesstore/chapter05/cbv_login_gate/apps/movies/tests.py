from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CBVLoginRequiredTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="alice123456")

    def test_cbv_redirects_when_not_logged_in(self):
        resp = self.client.get(reverse("movies:vip_cbv"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp.url)
        self.assertIn("next=", resp.url)

    def test_cbv_allows_after_login(self):
        self.client.login(username="alice", password="alice123456")
        resp = self.client.get(reverse("movies:vip_cbv"))
        self.assertEqual(resp.status_code, 200)

    def test_mro_contains_loginrequiredmixin_first(self):
        # VipCBVView(LoginRequiredMixin, TemplateView) 的 MRO 应该先出现 LoginRequiredMixin
        from apps.movies.views import VipCBVView
        mro_names = [c.__name__ for c in VipCBVView.mro()]
        self.assertTrue(mro_names.index("LoginRequiredMixin") < mro_names.index("TemplateView"))