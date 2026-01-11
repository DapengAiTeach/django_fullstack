from rest_framework.test import APITestCase
from rest_framework import status
from apps.movies.models import Movie


class FilterSearchOrderingPaginationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(title="星际穿越", genre="SCI_FI", year=2014, rating="9.2", is_hot=True)
        Movie.objects.create(title="盗梦空间", genre="SCI_FI", year=2010, rating="9.0", is_hot=True)
        Movie.objects.create(title="速度与激情7", genre="ACTION", year=2015, rating="8.2", is_hot=False)
        Movie.objects.create(title="速度与激情8", genre="ACTION", year=2017, rating="7.1", is_hot=False)
        Movie.objects.create(title="疯狂动物城", genre="COMEDY", year=2016, rating="8.4", is_hot=True)

    def test_filterset_fields_should_work(self):
        r = self.client.get("/api/movies/?genre=ACTION")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        titles = [x["title"] for x in r.data["data"]["results"]]
        self.assertIn("速度与激情7", titles)

    def test_search_filter_should_work(self):
        r = self.client.get("/api/movies/?search=星际")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        titles = [x["title"] for x in r.data["data"]["results"]]
        self.assertIn("星际穿越", titles)

    def test_ordering_filter_should_work(self):
        r = self.client.get("/api/movies/?ordering=-rating")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        results = r.data["data"]["results"]
        self.assertGreaterEqual(float(results[0]["rating"]), float(results[-1]["rating"]))

    def test_multi_condition_should_work(self):
        r = self.client.get("/api/movies/?genre=SCI_FI&year=2014&rating__gte=8.5&search=星&ordering=-rating")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        results = r.data["data"]["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "星际穿越")

    def test_page_number_pagination_should_work(self):
        r = self.client.get("/api/movies/?p=page&page=1&page_size=2&ordering=-created_at")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        self.assertEqual(len(r.data["data"]["results"]), 2)
        self.assertEqual(r.data["data"]["pagination"]["mode"], "page")