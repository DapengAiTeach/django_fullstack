from django.test import TestCase
from django.urls import reverse
from apps.movies.models import Genre, Movie

class MoviesBasicTests(TestCase):
    def test_home_page_ok(self):
        resp = self.client.get(reverse("movies:home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Movies Admin Demo")

    def test_model_create(self):
        g = Genre.objects.create(name="测试类型")
        m = Movie.objects.create(title="测试电影", genre=g, price=12.34, is_published=True)
        self.assertEqual(str(m), "测试电影")