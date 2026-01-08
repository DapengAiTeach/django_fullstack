"""
关系模型数据初始化脚本（可独立运行）
------------------------------------------------
执行：
python scripts/init_data.py

功能：
- 清空并初始化：
  Director（1）
  Movie（N） -> ForeignKey 导演（1对多）
  User（1） -> Profile（1对1）
  Order（N） + OrderItem（中间表带额外字段）（多对多）
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

from django.contrib.auth import get_user_model
from django.db import transaction
from movies.models import Director, Movie, Order, OrderItem
from accounts.models import Profile

User = get_user_model()

DIRECTORS = ["诺兰", "斯皮尔伯格", "昆汀", "王家卫", "姜文"]
MOVIES = [
    "星际穿越", "盗梦空间", "黑客帝国", "低俗小说", "无间道",
    "阿甘正传", "教父", "泰坦尼克号", "霸王别姬", "流浪地球",
]

def main():
    print("🚀 开始初始化关系数据...")

    # 清理顺序：先清中间表，再清主表（避免外键约束）
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Movie.objects.all().delete()
    Director.objects.all().delete()

    # 用户/资料：谨慎处理（教学环境可直接清）
    Profile.objects.all().delete()
    User.objects.filter(username__in=["demo"]).delete()

    # 1) 创建用户 + Profile（一对一）
    user = User.objects.create_user(username="demo", password="123456")
    Profile.objects.create(user=user, nickname="演示账号", vip_level=2)
    print("✅ 已创建用户 demo / 123456 + Profile")

    # 2) 创建导演 + 电影（一对多）
    directors = []
    for name in DIRECTORS:
        directors.append(Director.objects.create(name=name))
    print(f"✅ 已创建导演 {len(directors)} 位")

    movies = []
    for i in range(30):
        d = random.choice(directors)
        title = random.choice(MOVIES) + f"·第{i+1}版"
        price = Decimal(random.randint(19, 99))
        movies.append(Movie(title=title, director=d, price=price))
    Movie.objects.bulk_create(movies)
    print(f"✅ 已创建电影 {len(movies)} 部（挂在导演名下）")

    # 3) 创建订单 + 订单项（多对多 + 中间表额外字段）
    all_movies = list(Movie.objects.all())

    with transaction.atomic():
        for _ in range(6):
            order = Order.objects.create(user=user)

            pick = random.sample(all_movies, k=random.randint(1, 4))
            items = []
            for m in pick:
                qty = random.randint(1, 3)
                items.append(
                    OrderItem(
                        order=order,
                        movie=m,
                        quantity=qty,
                        deal_price=m.price,  # 成交价快照
                    )
                )
            OrderItem.objects.bulk_create(items)

    print("✅ 已创建订单 6 个（含 OrderItem 明细）")
    print("✨ 初始化完成！你现在可以：")
    print("   1) /movies/ 查看电影列表（导演一对多）")
    print("   2) /movies/<id>/ 看反向查询（director.movies）")
    print("   3) /admin/ 用 demo/123456 登录后，再访问 /orders/new/ 创建订单")

if __name__ == "__main__":
    main()