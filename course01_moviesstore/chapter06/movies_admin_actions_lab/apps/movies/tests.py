from django.test import TestCase
from django.contrib.auth.models import User
from apps.movies.models import Movie

class ActionTest(TestCase):
    def test_movie_create(self):
        u = User.objects.create_user("u1")
        m = Movie.objects.create(title="测试片", price=10, created_by=u)
        self.assertEqual(str(m), "测试片")