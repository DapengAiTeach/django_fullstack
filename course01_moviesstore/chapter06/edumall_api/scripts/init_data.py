"""
初始化示例数据

要求：
- 脚本必须放在项目根目录 scripts/ 目录下
- 必须在项目根目录执行：python scripts/init_data.py
- 内置 sys.path.insert + 设置 DJANGO_SETTINGS_MODULE，避免 ModuleNotFoundError

运行顺序要求（与工程一致）：
1) python manage.py migrate
2) python scripts/init_data.py
"""

import os
import sys
from pathlib import Path

# ------------------------------------------------------------
# 将项目根目录加入 sys.path
# 解释：
# - 独立脚本不是通过 manage.py 启动，Python 不一定能找到 config/settings.py
# - 将根目录加入 sys.path 后，才能 import config / apps.xxx 等模块
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# ------------------------------------------------------------
# 指定 Django 配置模块
# ------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from apps.catalog.models import Product  # noqa: E402
from apps.reviews.models import Review  # noqa: E402


def main():
    """
    数据策略：
    - 使用 get_or_create 保证可重复执行，不产生重复数据（幂等）
    - Review 依赖 Product，先创建 Product 再创建 Review
    """

    products_seed = [
        {"title": "Django 企业开发实战", "sku": "DJANGO-001", "price": "99.00", "stock": 100, "is_active": True},
        {"title": "DRF API 设计指南", "sku": "DRF-001", "price": "129.00", "stock": 50, "is_active": True},
    ]

    created_products = 0
    for item in products_seed:
        obj, created = Product.objects.get_or_create(
            sku=item["sku"],
            defaults=item,
        )
        created_products += 1 if created else 0

    # 取出商品用于创建评价
    p1 = Product.objects.get(sku="DJANGO-001")
    p2 = Product.objects.get(sku="DRF-001")

    reviews_seed = [
        {"product": p1, "rating": 5, "content": "内容扎实，工程化细节很多。", "author_display": "张三"},
        {"product": p1, "rating": 5, "content": "适合直接落地做项目。", "author_display": "李四"},
        {"product": p2, "rating": 4, "content": "体系清晰，示例贴近真实业务。", "author_display": "王五"},
    ]

    created_reviews = 0
    for item in reviews_seed:
        # 使用 (product, content) 做幂等键（示例），避免重复插入
        obj, created = Review.objects.get_or_create(
            product=item["product"],
            content=item["content"],
            defaults={
                "rating": item["rating"],
                "author_display": item["author_display"],
            },
        )
        created_reviews += 1 if created else 0

    print(f"[init_data] products_created={created_products}, reviews_created={created_reviews}")
    print(f"[init_data] product_total={Product.objects.count()}, review_total={Review.objects.count()}")


if __name__ == "__main__":
    main()