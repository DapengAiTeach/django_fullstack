"""
ORM 性能优化实验室：初始化数据（可独立运行）
----------------------------------------
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

from movies.models import Director, Tag, Movie, Review

DIRECTORS = ["诺兰", "斯皮尔伯格", "昆汀", "王家卫", "姜文"]
TAGS = ["科幻", "动作", "悬疑", "文艺", "热血", "烧脑", "治愈", "经典"]
MOVIES = ["星际穿越", "盗梦空间", "黑客帝国", "低俗小说", "无间道", "阿甘正传", "教父", "霸王别姬"]
COMMENTS = ["太好看了！", "节奏很舒服", "细节爆炸", "值得二刷", "镜头语言绝了", "剧情反转精彩", "配乐封神"]

def main():
    print("🚀 初始化数据...")

    # 清理顺序：先子表再父表
    Review.objects.all().delete()
    Movie.tags.through.objects.all().delete()  # M2M 中间表
    Movie.objects.all().delete()
    Tag.objects.all().delete()
    Director.objects.all().delete()

    directors = [Director.objects.create(name=n) for n in DIRECTORS]
    tags = [Tag.objects.create(name=n) for n in TAGS]

    movies = []
    for i in range(60):
        d = random.choice(directors)
        title = random.choice(MOVIES) + f" · 第{i+1}版"
        movies.append(Movie(title=title, director=d))
    Movie.objects.bulk_create(movies)

    all_movies = list(Movie.objects.all())

    # 绑定标签（M2M）
    for m in all_movies:
        pick = random.sample(tags, k=random.randint(1, 4))
        m.tags.add(*pick)

    # 创建评论（反向集合）
    reviews = []
    for _ in range(600):
        m = random.choice(all_movies)
        reviews.append(
            Review(
                movie=m,
                nickname=f"用户{random.randint(1, 999)}",
                score=random.randint(1, 10),
                content=random.choice(COMMENTS),
            )
        )
    Review.objects.bulk_create(reviews)

    print("✅ 导演：", Director.objects.count())
    print("✅ 标签：", Tag.objects.count())
    print("✅ 电影：", Movie.objects.count())
    print("✅ 评论：", Review.objects.count())
    print("✨ 完成！访问 /movies/ 对比 slow/fast/split 三种模式。")

if __name__ == "__main__":
    main()