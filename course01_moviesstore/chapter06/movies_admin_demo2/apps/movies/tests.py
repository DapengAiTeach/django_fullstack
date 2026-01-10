from django.test import TestCase
from django.urls import reverse
from apps.movies.models import Genre, Director, Movie

class MoviesAdminDemoTests(TestCase):
    def test_home_page_ok(self):
        resp = self.client.get(reverse("movies:home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Movies Admin Demo")

    def test_models_ok(self):
        g = Genre.objects.create(name="测试类型")
        d = Director.objects.create(name="测试导演", country="CN")
        m = Movie.objects.create(title="测试电影", genre=g, director=d, price=12.34)
        self.assertEqual(str(m), "测试电影")