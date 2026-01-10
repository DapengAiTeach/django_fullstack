from django.test import TestCase
from apps.movies.models import Movie

class AdminFormsLabTests(TestCase):
    def test_movie_create(self):
        m = Movie.objects.create(title="测试电影", price=10.00, discount=10, final_price=9.00, is_published=True)
        self.assertEqual(str(m), "测试电影")