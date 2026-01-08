from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from movies.models import Movie

User = get_user_model()

class AuthzTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="alice123456")
        self.bob = User.objects.create_user(username="bob", password="bob123456")

        ct = ContentType.objects.get_for_model(Movie)
        self.perm_add = Permission.objects.get(content_type=ct, codename="add_movie")
        self.perm_change = Permission.objects.get(content_type=ct, codename="change_movie")

        self.movie = Movie.objects.create(title="A", year=2020, summary="x", owner=self.alice)

    def test_anonymous_cannot_create(self):
        url = reverse("movies:movie_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # 被重定向到登录页（login_required）

    def test_user_without_perm_cannot_create(self):
        self.client.login(username="alice", password="alice123456")
        url = reverse("movies:movie_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)  # permission_required raise_exception=True

    def test_user_with_add_perm_can_create(self):
        self.alice.user_permissions.add(self.perm_add)
        self.client.login(username="alice", password="alice123456")

        url = reverse("movies:movie_create")
        resp = self.client.post(url, data={"title": "New", "year": 2021, "summary": "ok"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Movie.objects.filter(title="New").exists())

    def test_object_owner_rule(self):
        # 给 bob change 权限，但他不是 owner
        self.bob.user_permissions.add(self.perm_change)
        self.client.login(username="bob", password="bob123456")

        url = reverse("movies:movie_update", args=[self.movie.pk])
        resp = self.client.get(url)
        # 我们在视图里用了 404 隐藏存在性
        self.assertEqual(resp.status_code, 404)