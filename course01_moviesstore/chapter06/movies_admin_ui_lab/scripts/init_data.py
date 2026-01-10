import os, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth.models import User
from apps.movies.models import Movie

def main():
    admin, _ = User.objects.get_or_create(
        username="admin",
        defaults={"is_superuser": True, "is_staff": True},
    )
    admin.set_password("admin123456")
    admin.save()

    for i in range(1, 6):
        Movie.objects.get_or_create(title=f"示例电影 {i}")

    print("初始化完成：admin / admin123456")

if __name__ == "__main__":
    main()