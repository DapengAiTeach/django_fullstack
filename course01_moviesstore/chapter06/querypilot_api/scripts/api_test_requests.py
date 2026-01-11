"""
QueryPilot API 自检脚本（幂等）

覆盖：
- filterset_fields（genre/year/is_hot/rating__gte）
- SearchFilter（search）
- OrderingFilter（ordering）
- 多条件组合
- 三种分页（p=page/limit/cursor）
"""

import sys
import requests

BASE = "http://127.0.0.1:8000/api"


def pretty(title, r: requests.Response):
    print("\n" + "=" * 70)
    print(title)
    print("status:", r.status_code)
    try:
        print("json:", r.json())
    except Exception:
        print("text:", r.text)


def assert_ok(r: requests.Response):
    if r.status_code != 200:
        pretty("ASSERT_FAIL", r)
        raise RuntimeError(f"HTTP != 200, got={r.status_code}")
    j = r.json()
    if j.get("code") != 0:
        pretty("ASSERT_FAIL", r)
        raise RuntimeError(f"code != 0, got={j.get('code')}")
    return j


def main():
    # 1) filter
    r = requests.get(f"{BASE}/movies/?genre=SCI_FI")
    pretty("GET /movies?genre=SCI_FI", r)
    j = assert_ok(r)

    # 2) search
    r = requests.get(f"{BASE}/movies/?search=星际")
    pretty("GET /movies?search=星际", r)
    j = assert_ok(r)

    # 3) ordering
    r = requests.get(f"{BASE}/movies/?ordering=-rating")
    pretty("GET /movies?ordering=-rating", r)
    j = assert_ok(r)

    # 4) multi condition
    r = requests.get(f"{BASE}/movies/?genre=SCI_FI&year=2014&rating__gte=8.5&search=星&ordering=-rating")
    pretty("GET /movies multi", r)
    j = assert_ok(r)

    # 5) PageNumberPagination
    r = requests.get(f"{BASE}/movies/?p=page&page=1&page_size=3")
    pretty("GET /movies p=page", r)
    j = assert_ok(r)
    if j["data"]["pagination"]["mode"] != "page":
        raise RuntimeError("pagination mode should be page")

    # 6) LimitOffsetPagination
    r = requests.get(f"{BASE}/movies/?p=limit&limit=3&offset=0")
    pretty("GET /movies p=limit", r)
    j = assert_ok(r)
    if j["data"]["pagination"]["mode"] != "limit":
        raise RuntimeError("pagination mode should be limit")

    # 7) CursorPagination（需要先拿 next cursor）
    r = requests.get(f"{BASE}/movies/?p=cursor&page_size=3&ordering=-created_at")
    pretty("GET /movies p=cursor first", r)
    j = assert_ok(r)
    if j["data"]["pagination"]["mode"] != "cursor":
        raise RuntimeError("pagination mode should be cursor")

    next_link = j["data"]["pagination"]["next"]
    if next_link:
        r = requests.get(next_link)
        pretty("GET /movies p=cursor next", r)
        j = assert_ok(r)

    print("\n[done] api checks passed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n[FAILED]", e)
        sys.exit(1)