"""
反向查询实验室：初始化数据（可独立运行）
---------------------------------------
执行：
python scripts/init_data.py
"""

import os
import sys
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from movies.models import Director, Movie, Review

DIRECTORS = ["诺兰", "斯皮尔伯格", "昆汀", "王家卫"]
MOVIES = ["星际穿越", "盗梦空间", "黑客帝国", "低俗小说", "无间道", "阿甘正传"]
COMMENTS = ["太牛了！", "节奏很舒服", "看完回味很久", "镜头语言绝了", "剧情反转精彩", "配乐封神"]

def main():
    print("🚀 初始化反向查询数据...")

    # 先清“子表”，再清“父表”
    Review.objects.all().delete()
    Movie.objects.all().delete()
    Director.objects.all().delete()

    directors = [Director.objects.create(name=n) for n in DIRECTORS]

    movies = []
    for i in range(18):
        d = random.choice(directors)
        title = random.choice(MOVIES) + f"·第{i+1}版"
        movies.append(Movie(title=title, director=d))
    Movie.objects.bulk_create(movies)

    all_movies = list(Movie.objects.all())
    reviews = []
    for _ in range(50):
        m = random.choice(all_movies)
        reviews.append(
            Review(
                movie=m,
                nickname=f"用户{random.randint(1, 99)}",
                score=random.randint(1, 10),
                content=random.choice(COMMENTS),
            )
        )
    Review.objects.bulk_create(reviews)

    print("✅ 导演：", Director.objects.count())
    print("✅ 电影：", Movie.objects.count())
    print("✅ 评论：", Review.objects.count())
    print("✨ 完成！访问 /directors/ 开始体验反向查询。")

if __name__ == "__main__":
    main()