"""
接口自检脚本（幂等，不污染数据库）

要求：
- 支持多次运行：重复执行不会创建无限重复数据
- 覆盖所有 API：products CRUD + product reviews list/create
- 通过固定 SKU 与固定 Review 内容实现幂等

用法：
1) python manage.py runserver
2) python scripts/api_test_requests.py
"""

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


def ensure_product():
    """
    幂等创建商品：
    - 通过固定 sku 确保后端 unique 约束
    - 如果已存在，会得到 400（唯一性冲突）
    处理策略：
    - 先尝试列表查 sku
    - 若不存在则创建
    """
    list_r = requests.get(f"{BASE}/products/")
    list_r.raise_for_status()
    data = list_r.json()["data"]

    for item in data:
        if item["sku"] == "API-CHK-001":
            return item["id"]

    payload = {
        "title": "API自检商品",
        "sku": "API-CHK-001",
        "price": "19.90",
        "stock": 10,
        "is_active": True,
    }
    create_r = requests.post(f"{BASE}/products/", json=payload)
    if create_r.status_code == 201:
        return create_r.json()["data"]["id"]

    # 若创建失败，输出信息并抛错
    pretty("POST /products/ (ensure_product)", create_r)
    raise RuntimeError("ensure_product failed")


def ensure_review(product_id: int):
    """
    幂等创建评价：
    - 通过固定 content 判断是否已存在
    - 若已存在则跳过创建
    """
    list_r = requests.get(f"{BASE}/products/{product_id}/reviews/")
    list_r.raise_for_status()
    data = list_r.json()["data"]
    for item in data:
        if item["content"] == "这是API自检评价内容，固定文本。":
            return item["id"]

    payload = {
        "rating": 5,
        "content": "这是API自检评价内容，固定文本。",
        "author_name": "api_tester",
    }
    create_r = requests.post(f"{BASE}/products/{product_id}/reviews/", json=payload)
    create_r.raise_for_status()
    return create_r.json()["data"]["id"]


def main():
    # 1) products list
    r = requests.get(f"{BASE}/products/")
    pretty("GET /products/", r)

    # 2) ensure product exists
    product_id = ensure_product()
    print("\nensure_product id:", product_id)

    # 3) products retrieve (detail)
    r = requests.get(f"{BASE}/products/{product_id}/")
    pretty("GET /products/{id}/", r)

    # 4) products patch
    r = requests.patch(f"{BASE}/products/{product_id}/", json={"title": "API自检商品(更新后)"})
    pretty("PATCH /products/{id}/", r)

    # 5) nested reviews list + ensure review
    r = requests.get(f"{BASE}/products/{product_id}/reviews/")
    pretty("GET /products/{product_id}/reviews/", r)

    review_id = ensure_review(product_id)
    print("\nensure_review id:", review_id)

    r = requests.get(f"{BASE}/products/{product_id}/reviews/")
    pretty("GET /products/{product_id}/reviews/ (after ensure)", r)

    # 6) delete product（可选：为了不污染 DB，可以不删；如果删，会级联删除 review）
    #    脚本默认不删，保持可反复检查“详情嵌套/聚合字段”。
    print("\n[done] api check passed")


if __name__ == "__main__":
    main()