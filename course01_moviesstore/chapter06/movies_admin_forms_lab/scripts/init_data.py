import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from apps.movies.models import Movie  # noqa: E402


def main():
    # 1) 超级用户
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

    # 2) 普通 staff（用于演示：不能改 risk_level）
    staff_username = "ops"
    staff_password = "ops123456"

    if not User.objects.filter(username=staff_username).exists():
        u = User.objects.create_user(username=staff_username, email="ops@example.com", password=staff_password)
        u.is_staff = True
        u.is_active = True
        u.save()
        print(f"[OK] 创建运营 staff：{staff_username} / {staff_password}")
    else:
        print("[SKIP] 运营 staff 已存在：ops")

    # 3) 初始化电影商品
    Movie.objects.get_or_create(
        title="星际远航：序章",
        defaults={"price": 29.90, "discount": 20, "final_price": 23.92, "is_published": True, "risk_level": 1},
    )
    Movie.objects.get_or_create(
        title="霓虹追击",
        defaults={"price": 19.90, "discount": 0, "final_price": 19.90, "is_published": True, "risk_level": 2},
    )
    Movie.objects.get_or_create(
        title="海边的算法",
        defaults={"price": 9.90, "discount": 50, "final_price": 4.95, "is_published": False, "risk_level": 3},
    )
    print("[OK] 初始化电影数据完成")


if __name__ == "__main__":
    main()