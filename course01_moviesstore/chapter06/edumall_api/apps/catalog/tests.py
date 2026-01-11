from rest_framework.test import APITestCase
from rest_framework import status

from apps.catalog.models import Product
from apps.reviews.models import Review


class ProductSerializerDeepTests(APITestCase):
    """
    目标：
    - 验证统一返回结构（ApiResponseMixin 生效）
    - 验证 Product 详情 serializer 的嵌套与自定义字段
    - 验证校验规则（对象级校验）
    """

    def test_create_product_should_validate_object_level_rule(self):
        """
        对象级校验规则：
        - is_active=True 时，stock 必须 > 0
        """
        payload = {
            "title": "测试商品",
            "sku": "test-001",
            "price": "10.00",
            "stock": 0,
            "is_active": True,
        }
        resp = self.client.post("/api/products/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 统一结构断言
        self.assertNotEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "validation_error")
        self.assertIn("stock", resp.data["data"])

    def test_product_detail_should_include_nested_and_method_fields(self):
        """
        Product 详情：
        - 包含 reviews（嵌套序列化）
        - 包含 review_count/avg_rating/is_hot（SerializerMethodField）
        """
        product = Product.objects.create(
            title="Django 书",
            sku="DJ-001",
            price="88.00",
            stock=10,
            is_active=True,
        )
        Review.objects.create(product=product, rating=5, content="内容扎实，很推荐。", author_display="A")
        Review.objects.create(product=product, rating=5, content="非常适合做项目。", author_display="B")

        resp = self.client.get(f"/api/products/{product.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data["code"], 0)
        data = resp.data["data"]

        self.assertIn("reviews", data)
        self.assertEqual(len(data["reviews"]), 2)

        self.assertIn("review_count", data)
        self.assertEqual(data["review_count"], 2)

        self.assertIn("avg_rating", data)
        self.assertIsNotNone(data["avg_rating"])

        self.assertIn("is_hot", data)
        self.assertEqual(data["is_hot"], True)