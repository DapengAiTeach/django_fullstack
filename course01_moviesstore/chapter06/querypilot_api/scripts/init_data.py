"""
初始化 Movie 测试数据（幂等）

执行：
- 在项目根目录运行：python scripts/init_data.py

幂等策略：
- 以 (title, year) 作为幂等键
- 已存在则更新字段，确保演示数据一致
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from apps.movies.models import Movie  # noqa: E402


def upsert_movie(title, genre, year, rating, is_hot):
    obj = Movie.objects.filter(title=title, year=year).first()
    if obj:
        obj.genre = genre
        obj.rating = rating
        obj.is_hot = is_hot
        obj.save(update_fields=["genre", "rating", "is_hot"])
        return obj
    return Movie.objects.create(title=title, genre=genre, year=year, rating=rating, is_hot=is_hot)


def main():
    seed = [
        ("星际穿越", "SCI_FI", 2014, 9.2, True),
        ("盗梦空间", "SCI_FI", 2010, 9.0, True),
        ("疯狂动物城", "COMEDY", 2016, 8.4, True),
        ("阿甘正传", "DRAMA", 1994, 9.5, True),
        ("速度与激情7", "ACTION", 2015, 8.2, False),
        ("速度与激情8", "ACTION", 2017, 7.1, False),
        ("银河护卫队", "SCI_FI", 2014, 8.1, False),
        ("喜剧之王", "COMEDY", 1999, 8.8, False),
        ("肖申克的救赎", "DRAMA", 1994, 9.7, True),
        ("流浪地球", "SCI_FI", 2019, 7.9, True),
    ]

    for item in seed:
        upsert_movie(*item)

    print(f"[init_data] movies total={Movie.objects.count()}")


if __name__ == "__main__":
    main()