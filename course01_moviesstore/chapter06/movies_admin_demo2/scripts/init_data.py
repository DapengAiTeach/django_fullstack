import os
import sys
from pathlib import Path

# ✅ 项目根目录（manage.py 所在目录）
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from apps.movies.models import Genre, Director, Tag, Movie  # noqa: E402


def main():
    # 1) 创建超级用户：用于登录 Django Admin
    admin_username = "admin"
    admin_password = "admin123456"

    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(
            username=admin_username,
            email="admin@example.com",
            password=admin_password,
        )
        print(f"[OK] 创建超级用户：{admin_username} / {admin_password}")
    else:
        print("[SKIP] 超级用户已存在：admin")

    # 2) 初始化基础数据：类型、导演、标签
    g_action, _ = Genre.objects.get_or_create(name="动作")
    g_scifi, _ = Genre.objects.get_or_create(name="科幻")
    g_drama, _ = Genre.objects.get_or_create(name="剧情")

    d1, _ = Director.objects.get_or_create(name="诺兰", defaults={"country": "英国"})
    d2, _ = Director.objects.get_or_create(name="斯皮尔伯格", defaults={"country": "美国"})
    d3, _ = Director.objects.get_or_create(name="是枝裕和", defaults={"country": "日本"})

    t_hot, _ = Tag.objects.get_or_create(name="爆款")
    t_new, _ = Tag.objects.get_or_create(name="新上架")
    t_award, _ = Tag.objects.get_or_create(name="获奖")

    # 3) 电影数据（用于验证 list_editable / filter / search / ordering）
    m1, _ = Movie.objects.get_or_create(
        title="星际远航：序章",
        defaults={
            "genre": g_scifi,
            "director": d1,
            "price": 29.90,
            "level": 3,
            "is_published": True,
            "stock": 120,
        },
    )
    m1.tags.set([t_hot, t_award])

    m2, _ = Movie.objects.get_or_create(
        title="霓虹追击",
        defaults={
            "genre": g_action,
            "director": d2,
            "price": 19.90,
            "level": 2,
            "is_published": True,
            "stock": 80,
        },
    )
    m2.tags.set([t_hot, t_new])

    m3, _ = Movie.objects.get_or_create(
        title="海边的算法",
        defaults={
            "genre": g_drama,
            "director": d3,
            "price": 9.90,
            "level": 1,
            "is_published": False,
            "stock": 30,
        },
    )
    m3.tags.set([t_award])

    print("[OK] 初始化数据完成：类型/导演/标签/电影")


if __name__ == "__main__":
    main()