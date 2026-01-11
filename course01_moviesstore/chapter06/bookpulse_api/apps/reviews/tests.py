from rest_framework.test import APITestCase
from rest_framework import status
from apps.reviews.models import Review


class ReviewApiTests(APITestCase):
    """
    TDD 核心：断言统一结构（code/message/data）+ CRUD 行为
    """

    def test_health_api_should_return_uniform_json(self):
        resp = self.client.get("/api/health/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "ok")
        self.assertEqual(resp.data["data"]["status"], "running")

    def test_list_reviews_should_return_uniform_json(self):
        Review.objects.create(book_title="测试书A", content="不错", rating=5)
        Review.objects.create(book_title="测试书B", content="还行", rating=4)

        resp = self.client.get("/api/reviews/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "ok")
        self.assertIsInstance(resp.data["data"], list)
        self.assertEqual(len(resp.data["data"]), 2)

    def test_create_review_should_work(self):
        payload = {
            "book_title": "新书",
            "content": "这是一本新书的书评",
            "rating": 5,
        }
        resp = self.client.post("/api/reviews/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "ok")
        self.assertEqual(resp.data["data"]["book_title"], "新书")

    def test_create_review_with_invalid_rating_should_fail(self):
        payload = {
            "book_title": "坏数据书评",
            "content": "评分不合法",
            "rating": 99,
        }
        resp = self.client.post("/api/reviews/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertNotEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "validation_error")
        self.assertIn("rating", resp.data["data"])

    def test_generic_list_api_should_work(self):
        Review.objects.create(book_title="Generic测试书", content="演示 GenericAPIView", rating=4)

        resp = self.client.get("/api/reviews-generic/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data["code"], 0)
        self.assertIsInstance(resp.data["data"], list)
        self.assertEqual(len(resp.data["data"]), 1)

    def test_retrieve_update_delete_review(self):
        review = Review.objects.create(book_title="可修改书评", content="原始内容", rating=3)

        # retrieve
        resp = self.client.get(f"/api/reviews/{review.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["data"]["book_title"], "可修改书评")

        # patch
        resp = self.client.patch(
            f"/api/reviews/{review.id}/",
            data={"rating": 4},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["data"]["rating"], 4)

        # delete
        resp = self.client.delete(f"/api/reviews/{review.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)