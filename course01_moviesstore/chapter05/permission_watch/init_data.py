import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.movies.models import Movie

User = get_user_model()

def main():
    # 1) 管理员
    admin, _ = User.objects.get_or_create(username="admin")
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin123456")
    admin.save()

    # 2) 普通用户
    alice, _ = User.objects.get_or_create(username="alice")
    alice.set_password("alice123456")
    alice.save()

    # 3) 初始化数据
    if not Movie.objects.exists():
        Movie.objects.create(title="星际穿越", year=2014)
        Movie.objects.create(title="盗梦空间", year=2010)

    # 4) 打印默认权限（从数据库 auth_permission 读取）
    ct = ContentType.objects.get_for_model(Movie)
    wanted = {"add_movie", "change_movie", "delete_movie", "view_movie"}

    perms = Permission.objects.filter(content_type=ct, codename__in=wanted).order_by("codename")
    print("✅ 初始化完成：")
    print("admin / admin123456")
    print("alice / alice123456")
    print("\n=== Movie 模型默认权限（来自数据库 auth_permission）===")
    for p in perms:
        # p.content_type.app_label + p.codename => app_label.codename
        print(f"- id={p.id}  key={p.content_type.app_label}.{p.codename}  name={p.name}")

if __name__ == "__main__":
    main()