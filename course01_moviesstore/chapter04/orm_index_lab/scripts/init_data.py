"""
索引与Meta实验室：初始化数据（可独立运行）
---------------------------------------
执行：
python scripts/init_data.py

数据特点：
- 造大量电影（便于体验索引在后台筛选/排序的价值）
- 造 SKU（触发 unique_together 的约束）
"""

import os
import sys
import random
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from movies.models import Director, Movie, MovieSKU

DIRECTORS = ["诺兰", "斯皮尔伯格", "昆汀", "王家卫", "姜文"]
CATEGORIES = ["科幻", "动作", "悬疑", "文艺", "喜剧", "犯罪"]
EDITIONS = ["HD", "4K", "DirectorCut"]

MOVIE_TITLES = ["星际穿越", "盗梦空间", "黑客帝国", "低俗小说", "无间道", "阿甘正传", "教父", "霸王别姬", "流浪地球"]


def main():
    print("🚀 初始化索引/Meta数据...")

    # 清理顺序：SKU -> Movie -> Director
    MovieSKU.objects.all().delete()
    Movie.objects.all().delete()
    Director.objects.all().delete()

    directors = [Director.objects.create(name=n) for n in DIRECTORS]

    movies = []
    for i in range(800):  # 数据多一点，才有索引感
        d = random.choice(directors)
        title = random.choice(MOVIE_TITLES) + f" · 第{i + 1}版"
        movies.append(
            Movie(
                title=title,
                director=d,
                category=random.choice(CATEGORIES),
                is_active=(random.random() < 0.75),
                rating=round(random.uniform(5.0, 9.8), 1),
            )
        )
    Movie.objects.bulk_create(movies)

    all_movies = list(Movie.objects.all())

    # 造 SKU：触发 unique_together(movie, edition)
    sku_rows = []
    for m in random.sample(all_movies, k=min(300, len(all_movies))):
        for ed in random.sample(EDITIONS, k=random.randint(1, 3)):
            sku_rows.append(
                MovieSKU(
                    movie=m,
                    edition=ed,
                    price=Decimal(random.randint(19, 99)),
                )
            )
    # bulk_create 遇到唯一冲突会报错，这里我们保证不会重复造同一电影同一版本
    MovieSKU.objects.bulk_create(sku_rows)

    print("✅ 导演：", Director.objects.count())
    print("✅ 电影：", Movie.objects.count())
    print("✅ SKU：", MovieSKU.objects.count())
    print("✨ 完成！访问 /movies/ 体验筛选排序。")


if __name__ == "__main__":
    main()
