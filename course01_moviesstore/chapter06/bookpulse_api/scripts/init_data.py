"""
初始化示例数据（防路径问题版本）

用法（必须在项目根目录执行）：
    cd bookpulse_api
    python scripts/init_data.py
"""

import os
import sys
from pathlib import Path

# -----------------------------
# 关键：加入项目根目录，防止 ModuleNotFoundError: config
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from apps.reviews.models import Review  # noqa: E402


def main():
    seed = [
        {
            "book_title": "高效能人士的七个习惯",
            "content": "一本关于自我管理与长期主义的经典。",
            "rating": 5,
        },
        {
            "book_title": "原则",
            "content": "把决策系统化，是成年人的必修课。",
            "rating": 4,
        },
        {
            "book_title": "人类简史",
            "content": "从宏观视角理解文明演进，很震撼。",
            "rating": 5,
        },
    ]

    created = 0
    for item in seed:
        obj, is_created = Review.objects.get_or_create(
            book_title=item["book_title"],
            defaults=item,
        )
        if is_created:
            created += 1

    print(f"[init_data] done. created={created}, total={Review.objects.count()}")


if __name__ == "__main__":
    main()