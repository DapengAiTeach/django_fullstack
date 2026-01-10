import os
import sys
from pathlib import Path
from decimal import Decimal
import random

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from apps.movies.models import Genre, Director, Movie  # noqa: E402


def main():
    # 1) 超级用户
    admin_username = "admin"
    admin_password = "admin123456"
    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(admin_username, "admin@example.com", admin_password)
        print(f"[OK] 创建超级用户：{admin_username} / {admin_password}")
    else:
        print("[SKIP] 超级用户已存在：admin")

    # 2) 运营 staff（用于验证：只看到自己 created_by 的数据）
    ops_username = "ops"
    ops_password = "ops123456"
    if not User.objects.filter(username=ops_username).exists():
        u = User.objects.create_user(ops_username, "ops@example.com", ops_password)
        u.is_staff = True
        u.is_active = True
        u.save()
        print(f"[OK] 创建运营 staff：{ops_username} / {ops_password}")
    else:
        print("[SKIP] 运营 staff 已存在：ops")

    admin_user = User.objects.get(username="admin")
    ops_user = User.objects.get(username="ops")

    # 3) 基础字典
    g_scifi, _ = Genre.objects.get_or_create(name="科幻")
    g_action, _ = Genre.objects.get_or_create(name="动作")
    g_drama, _ = Genre.objects.get_or_create(name="剧情")

    d_nolan, _ = Director.objects.get_or_create(name="诺兰")
    d_spiel, _ = Director.objects.get_or_create(name="斯皮尔伯格")
    d_koreeda, _ = Director.objects.get_or_create(name="是枝裕和")

    # 4) 演示数据（含海报URL，可为空）
    seeds = [
        ("星际远航：序章", g_scifi, d_nolan, Decimal("29.90"), Decimal("8.8"), 3, "https://picsum.photos/200/280?random=11", admin_user),
        ("霓虹追击", g_action, d_spiel, Decimal("19.90"), Decimal("7.9"), 3, "https://picsum.photos/200/280?random=12", admin_user),
        ("海边的算法", g_drama, d_koreeda, Decimal("9.90"), Decimal("7.2"), 2, "https://picsum.photos/200/280?random=13", ops_user),
        ("量子回声", g_scifi, d_nolan, Decimal("59.90"), Decimal("8.3"), 2, "", ops_user),
        ("暗影跑道", g_action, d_spiel, Decimal("49.90"), Decimal("6.8"), 4, "", ops_user),
    ]

    for title, genre, director, price, score, status, poster, owner in seeds:
        Movie.objects.get_or_create(
            title=title,
            defaults={
                "genre": genre,
                "director": director,
                "price": price,
                "score": score,
                "status": status,
                "poster_url": poster,
                "created_by": owner,
            },
        )

    # 5) 再批量生成一些记录，方便看分页/筛选/搜索
    genres = [g_scifi, g_action, g_drama]
    directors = [d_nolan, d_spiel, d_koreeda]
    owners = [admin_user, ops_user]
    for i in range(1, 61):
        Movie.objects.get_or_create(
            title=f"运营样本片-{i:03d}",
            defaults={
                "genre": random.choice(genres),
                "director": random.choice(directors),
                "price": Decimal(str(random.choice([9.9, 19.9, 29.9, 49.9, 59.9]))),
                "score": Decimal(str(random.choice([6.2, 6.8, 7.4, 7.9, 8.6, 9.1]))),
                "status": random.choice([1, 2, 3, 4]),
                "poster_url": "" if i % 3 else f"https://picsum.photos/200/280?random={100+i}",
                "created_by": random.choice(owners),
            },
        )

    print("[OK] 初始化完成：类型/导演/电影/运营样本数据")


if __name__ == "__main__":
    main()