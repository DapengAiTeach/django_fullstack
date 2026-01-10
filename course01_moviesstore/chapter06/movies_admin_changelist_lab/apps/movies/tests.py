from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User
from apps.movies.models import Genre, Director, Movie

class ChangelistLabTests(TestCase):
    def test_models_create(self):
        u = User.objects.create_user("u1", "u1@example.com", "123456")
        g = Genre.objects.create(name="测试类型")
        d = Director.objects.create(name="测试导演")
        m = Movie.objects.create(
            title="测试电影",
            genre=g,
            director=d,
            price=Decimal("12.34"),
            score=Decimal("8.5"),
            status=3,
            created_by=u,
        )
        self.assertEqual(str(m), "测试电影")