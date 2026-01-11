from rest_framework.test import APITestCase
from rest_framework import status
from apps.movies.models import Movie


class MovieApiTests(APITestCase):
    """
    这些测试覆盖：
    - RESTful 的列表、创建、详情、更新、删除
    - JSON 返回结构是否统一（code/message/data）
    - 基础字段校验（rating 0~10）
    """

    def test_list_movies_should_return_uniform_json(self):
        Movie.objects.create(title="测试电影A", rating=8.5)
        Movie.objects.create(title="测试电影B", rating=7.0)

        resp = self.client.get("/api/movies/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # 统一结构断言
        self.assertIn("code", resp.data)
        self.assertIn("message", resp.data)
        self.assertIn("data", resp.data)

        self.assertEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "ok")
        self.assertIsInstance(resp.data["data"], list)
        self.assertEqual(len(resp.data["data"]), 2)

    def test_create_movie_should_work(self):
        payload = {
            "title": "新电影",
            "overview": "这是一部新电影",
            "release_date": "2020-01-01",
            "rating": 9.0,
        }
        resp = self.client.post("/api/movies/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # 统一结构断言
        self.assertEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "ok")
        self.assertEqual(resp.data["data"]["title"], "新电影")

    def test_create_movie_with_invalid_rating_should_fail(self):
        payload = {
            "title": "坏数据电影",
            "rating": 99.0,
        }
        resp = self.client.post("/api/movies/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 统一结构断言（错误时 code != 0）
        self.assertNotEqual(resp.data["code"], 0)
        self.assertEqual(resp.data["message"], "validation_error")
        self.assertIn("rating", resp.data["data"])

    def test_retrieve_update_delete_movie(self):
        movie = Movie.objects.create(title="可修改电影", rating=6.5)

        # retrieve
        resp = self.client.get(f"/api/movies/{movie.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["data"]["title"], "可修改电影")

        # update (PATCH)
        resp = self.client.patch(f"/api/movies/{movie.id}/", data={"rating": 7.5}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["data"]["rating"], "7.5")  # DecimalField 常以字符串返回

        # delete
        resp = self.client.delete(f"/api/movies/{movie.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # ensure deleted
        resp = self.client.get(f"/api/movies/{movie.id}/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)