"""
用法：
1）先启动服务：python manage.py runserver
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
    # health
    r = requests.get(f"{BASE}/health/")
    pretty("GET /health/", r)

    # list
    r = requests.get(f"{BASE}/reviews/")
    pretty("GET /reviews/", r)

    # create
    payload = {
        "book_title": "requests 创建书评",
        "content": "用 requests 直接调用 API",
        "rating": 5,
    }
    r = requests.post(f"{BASE}/reviews/", json=payload)
    pretty("POST /reviews/", r)

    review_id = r.json()["data"]["id"]

    # retrieve
    r = requests.get(f"{BASE}/reviews/{review_id}/")
    pretty("GET /reviews/{id}/", r)

    # patch
    r = requests.patch(f"{BASE}/reviews/{review_id}/", json={"rating": 4})
    pretty("PATCH /reviews/{id}/", r)

    # delete
    r = requests.delete(f"{BASE}/reviews/{review_id}/")
    pretty("DELETE /reviews/{id}/", r)

    # generic list
    r = requests.get(f"{BASE}/reviews-generic/")
    pretty("GET /reviews-generic/", r)


if __name__ == "__main__":
    main()