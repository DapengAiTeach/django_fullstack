from rest_framework.test import APITestCase
from rest_framework import status

from apps.catalog.models import Product
from apps.reviews.models import Review


class ReviewSerializerDeepTests(APITestCase):
    """
    目标：
    - 验证 Serializer（非 ModelSerializer）的 create() 逻辑
    - 验证 write_only/read_only 行为：
      - author_name 只写不出
      - author_display 只出不写（由 author_name 映射）
    - 验证幂等测试风格：每个测试使用独立数据库事务（APITestCase 自带）
    """

    def test_create_review_should_map_author_name_to_author_display(self):
        product = Product.objects.create(
            title="DRF 书",
            sku="DRF-001",
            price="100.00",
            stock=10,
            is_active=True,
        )

        payload = {
            "rating": 5,
            "content": "至少五个字以上。",
            "author_name": "测试作者",
        }
        resp = self.client.post(f"/api/products/{product.id}/reviews/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(resp.data["code"], 0)
        data = resp.data["data"]

        # 输出使用 ReviewReadSerializer
        self.assertIn("author_display", data)
        self.assertEqual(data["author_display"], "测试作者")

        # write_only 字段不应出现在输出中
        self.assertNotIn("author_name", data)

        # 数据库落库验证
        self.assertEqual(Review.objects.count(), 1)

    def test_create_review_should_validate_rating_and_content(self):
        product = Product.objects.create(
            title="DRF 书",
            sku="DRF-002",
            price="100.00",
            stock=10,
            is_active=True,
        )

        payload = {
            "rating": 9,           # 非法
            "content": "短",        # 非法（不足 5）
            "author_name": "",
        }
        resp = self.client.post(f"/api/products/{product.id}/reviews/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertNotEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "validation_error")

        # 两类错误都应返回
        self.assertIn("rating", resp.data["data"])
        self.assertIn("content", resp.data["data"])