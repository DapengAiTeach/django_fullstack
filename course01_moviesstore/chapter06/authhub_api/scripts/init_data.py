"""
初始化账号数据

执行：
- 在项目根目录运行：python scripts/init_data.py
- 脚本幂等：重复执行不会重复创建用户（按 username 判断）

创建用户：
- admin / admin123456（staff/superuser）
- alice / 123456
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()


def ensure_user(username: str, password: str, is_superuser=False, is_staff=False):
    user = User.objects.filter(username=username).first()
    if user:
        return user

    if is_superuser:
        user = User.objects.create_superuser(username=username, password=password)
    else:
        user = User.objects.create_user(username=username, password=password)

    user.is_staff = is_staff or is_superuser
    user.save()
    return user


def main():
    ensure_user("admin", "admin123456", is_superuser=True, is_staff=True)
    ensure_user("alice", "123456")

    print("[init_data] users ready: admin / alice")


if __name__ == "__main__":
    main()