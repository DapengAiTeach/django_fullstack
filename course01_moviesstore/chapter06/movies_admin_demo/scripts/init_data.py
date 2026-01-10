import os
import sys
from pathlib import Path

# ✅ 关键：无论你从哪里运行脚本，都先定位到项目根目录（manage.py 所在目录）
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# ✅ 关键：指向正确的 settings 模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from apps.movies.models import Genre, Movie  # noqa: E402


def main():
    # 1) 创建超级用户（用于 /admin 与 /ops 登录）
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

    # 2) 创建一个前台演示用户（非 staff）
    demo_username = "demo"
    demo_password = "demo123456"

    if not User.objects.filter(username=demo_username).exists():
        u = User(username=demo_username, email="demo@example.com", is_active=True)
        u.set_password(demo_password)
        u.save()
        print(f"[OK] 创建演示用户：{demo_username} / {demo_password}")
    else:
        print("[SKIP] 演示用户已存在：demo")

    # 3) 初始化类型与电影数据
    g_action, _ = Genre.objects.get_or_create(name="动作")
    g_scifi, _ = Genre.objects.get_or_create(name="科幻")
    g_drama, _ = Genre.objects.get_or_create(name="剧情")

    Movie.objects.get_or_create(
        title="星际远航：序章",
        genre=g_scifi,
        defaults={"price": 29.90, "is_published": True},
    )
    Movie.objects.get_or_create(
        title="霓虹追击",
        genre=g_action,
        defaults={"price": 19.90, "is_published": True},
    )
    Movie.objects.get_or_create(
        title="海边的算法",
        genre=g_drama,
        defaults={"price": 9.90, "is_published": False},
    )

    print("[OK] 初始化电影数据完成")


if __name__ == "__main__":
    main()
