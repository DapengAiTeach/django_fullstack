"""
初始化示例数据（防路径问题版本）

用法（推荐）：
    cd cinebox_api
    python scripts/init_data.py
"""

import os
import sys
from pathlib import Path

# -----------------------------
# 关键修复点：手动把项目根目录加入 sys.path
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from datetime import date  # noqa: E402
from apps.movies.models import Movie  # noqa: E402


def main():
    seed = [
        {
            "title": "流浪地球",
            "overview": "当太阳即将毁灭，人类开启流浪地球计划。",
            "release_date": date(2019, 2, 5),
            "rating": 8.0,
        },
        {
            "title": "让子弹飞",
            "overview": "一场关于正义、权力与人性的荒诞博弈。",
            "release_date": date(2010, 12, 16),
            "rating": 8.8,
        },
        {
            "title": "星际穿越",
            "overview": "为了人类的未来，穿越虫洞寻找新家园。",
            "release_date": date(2014, 11, 12),
            "rating": 9.2,
        },
    ]

    created = 0
    for item in seed:
        obj, is_created = Movie.objects.get_or_create(
            title=item["title"],
            defaults=item,
        )
        if is_created:
            created += 1

    print(f"[init_data] done. created={created}, total={Movie.objects.count()}")


if __name__ == "__main__":
    main()
