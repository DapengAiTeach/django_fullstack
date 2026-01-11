"""
用法：
1）先 python manage.py runserver
2）再执行：python scripts/api_test_requests.py
"""

import requests

BASE = "http://127.0.0.1:8000/api"


def pretty(title, r: requests.Response):
    print("\n" + "=" * 60)
    print(title)
    print("status:", r.status_code)
    try:
        print("json:", r.json())
    except Exception:
        print("text:", r.text)


def main():
    # list
    r = requests.get(f"{BASE}/movies/")
    pretty("GET /movies/", r)

    # create
    payload = {
        "title": "requests 创建的电影",
        "overview": "用 requests 直接调用 API",
        "release_date": "2021-01-01",
        "rating": 8.6,
    }
    r = requests.post(f"{BASE}/movies/", json=payload)
    pretty("POST /movies/", r)

    movie_id = r.json()["data"]["id"]

    # retrieve
    r = requests.get(f"{BASE}/movies/{movie_id}/")
    pretty("GET /movies/{id}/", r)

    # patch
    r = requests.patch(f"{BASE}/movies/{movie_id}/", json={"rating": 9.1})
    pretty("PATCH /movies/{id}/", r)

    # delete
    r = requests.delete(f"{BASE}/movies/{movie_id}/")
    pretty("DELETE /movies/{id}/", r)

    # verify deleted
    r = requests.get(f"{BASE}/movies/{movie_id}/")
    pretty("GET /movies/{id}/ after delete", r)


if __name__ == "__main__":
    main()