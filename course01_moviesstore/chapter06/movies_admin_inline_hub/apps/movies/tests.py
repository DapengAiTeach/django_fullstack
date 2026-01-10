from decimal import Decimal
from django.test import TestCase
from apps.movies.models import Movie, Order, OrderItem

class InlineHubTests(TestCase):
    def test_models_ok(self):
        m = Movie.objects.create(title="测试电影", price=Decimal("10.00"))
        o = Order.objects.create(order_no="NO0001", customer_name="张三", status=1)
        it = OrderItem.objects.create(order=o, movie=m, quantity=2, unit_price=Decimal("10.00"), line_total=Decimal("20.00"))
        self.assertEqual(str(o), "NO0001")
        self.assertIn("测试电影", str(it))