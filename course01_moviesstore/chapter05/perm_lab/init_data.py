import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perm_lab.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from movies.models import Movie

User = get_user_model()

def main():
    # 1) 创建用户
    admin, _ = User.objects.get_or_create(username="admin")
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin123456")
    admin.save()

    alice, _ = User.objects.get_or_create(username="alice")
    alice.is_staff = False
    alice.is_superuser = False
    alice.set_password("alice123456")
    alice.save()

    # 2) 创建角色（Group = 角色）
    editor, _ = Group.objects.get_or_create(name="Editor")        # 编辑
    moderator, _ = Group.objects.get_or_create(name="Moderator")  # 管理

    # 3) 取 Movie 对应的权限（Permission 存在 auth_permission 表）
    #    Permission 与模型的关联通过 ContentType（contenttypes 表）完成
    ct = ContentType.objects.get_for_model(Movie)

    # 默认权限（Django 自动生成）
    add_movie = Permission.objects.get(content_type=ct, codename="add_movie")
    change_movie = Permission.objects.get(content_type=ct, codename="change_movie")
    delete_movie = Permission.objects.get(content_type=ct, codename="delete_movie")
    view_movie = Permission.objects.get(content_type=ct, codename="view_movie")

    # 自定义权限（来自 Meta.permissions）
    publish_movie = Permission.objects.get(content_type=ct, codename="publish_movie")
    export_movie = Permission.objects.get(content_type=ct, codename="export_movie")

    # 4) 给角色分配权限（角色 = 一组权限的集合）
    editor.permissions.set([add_movie, change_movie, view_movie, publish_movie])
    moderator.permissions.set([delete_movie, view_movie, export_movie])

    # 5) 给用户分配角色（用户属于多个角色）
    alice.groups.set([editor])

    # 6) 演示：给用户“单独”塞一个权限（不通过 Group）
    #    例如：让 alice 具备 export_movie（即使 Editor 角色没有）
    alice.user_permissions.add(export_movie)

    # 7) 初始化一些电影数据
    if not Movie.objects.exists():
        Movie.objects.create(title="星际穿越", year=2014)
        Movie.objects.create(title="盗梦空间", year=2010)
        Movie.objects.create(title="流浪地球", year=2019)

    print("✅ 初始化完成")
    print("admin / admin123456（超级管理员）")
    print("alice / alice123456（Editor 角色 + 单独 export_movie 权限）")

if __name__ == "__main__":
    main()