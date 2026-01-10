import os
import sys
from pathlib import Path
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from apps.movies.models import Movie  # noqa: E402


def main():
    # 超级用户
    admin_username = "admin"
    admin_password = "admin123456"
    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(admin_username, "admin@example.com", admin_password)
        print(f"[OK] 创建超级用户：{admin_username} / {admin_password}")
    else:
        print("[SKIP] 超级用户已存在：admin")

    # 运营 staff（用于演示：没有删除 Inline 权限）
    staff_username = "ops"
    staff_password = "ops123456"
    if not User.objects.filter(username=staff_username).exists():
        u = User.objects.create_user(staff_username, "ops@example.com", staff_password)
        u.is_staff = True
        u.is_active = True
        u.save()
        print(f"[OK] 创建运营 staff：{staff_username} / {staff_password}")
    else:
        print("[SKIP] 运营 staff 已存在：ops")

    # 商品初始化（下单用）
    Movie.objects.get_or_create(title="星际远航：序章", defaults={"price": Decimal("29.90"), "is_published": True})
    Movie.objects.get_or_create(title="霓虹追击", defaults={"price": Decimal("19.90"), "is_published": True})
    Movie.objects.get_or_create(title="海边的算法", defaults={"price": Decimal("9.90"), "is_published": True})
    print("[OK] 初始化电影商品完成")


if __name__ == "__main__":
    main()