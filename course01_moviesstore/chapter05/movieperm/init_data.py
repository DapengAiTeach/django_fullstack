import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieperm.settings")
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from movies.models import Movie

User = get_user_model()

def main():
    # 1) 创建用户
    admin, _ = User.objects.get_or_create(username="admin")
    admin.is_superuser = True
    admin.is_staff = True
    admin.set_password("admin123456")
    admin.save()

    alice, _ = User.objects.get_or_create(username="alice")
    alice.is_staff = False
    alice.set_password("alice123456")
    alice.save()

    # 2) 创建角色（Group）
    editor, _ = Group.objects.get_or_create(name="Editor")
    moderator, _ = Group.objects.get_or_create(name="Moderator")

    # 3) 获取 Movie 的权限（默认 add/change/delete/view + 自定义权限）
    ct = ContentType.objects.get_for_model(Movie)

    perm_add = Permission.objects.get(content_type=ct, codename="add_movie")
    perm_change = Permission.objects.get(content_type=ct, codename="change_movie")
    perm_delete = Permission.objects.get(content_type=ct, codename="delete_movie")
    perm_view = Permission.objects.get(content_type=ct, codename="view_movie")

    perm_publish = Permission.objects.get(content_type=ct, codename="publish_movie")
    perm_export = Permission.objects.get(content_type=ct, codename="export_movie")

    # 4) 分配权限到角色
    editor.permissions.set([perm_add, perm_change, perm_view, perm_publish])
    moderator.permissions.set([perm_delete, perm_view, perm_export])

    # 5) 给 alice 绑定 Editor 角色
    alice.groups.add(editor)

    # 6) 初始化业务数据
    if not Movie.objects.exists():
        Movie.objects.create(title="星际穿越", year=2014, summary="关于爱与引力的硬科幻经典。", owner=alice)
        Movie.objects.create(title="盗梦空间", year=2010, summary="梦中梦结构与时间张力。", owner=alice)
        Movie.objects.create(title="流浪地球", year=2019, summary="行星发动机点燃中国科幻热。", owner=admin)

    print("✅ 初始化完成")
    print("admin / admin123456（超级管理员）")
    print("alice / alice123456（Editor：可新增/编辑/查看 + publish）")

if __name__ == "__main__":
    main()