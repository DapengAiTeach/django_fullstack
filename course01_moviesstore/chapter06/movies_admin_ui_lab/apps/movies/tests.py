from django.test import TestCase
from apps.movies.models import Movie

class AdminUITest(TestCase):
    def test_movie_str(self):
        m = Movie.objects.create(title="测试电影")
        self.assertEqual(str(m), "测试电影")