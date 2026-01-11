"""
初始化用户与文章数据（幂等）

执行：
- 在项目根目录运行：python scripts/init_data.py

策略：
- 用户按 username 幂等
- 文章按 (author, title) 幂等
- 幂等保证脚本可多次运行不污染数据库

创建：
- admin/admin123456（staff/superuser）
- alice/123456（普通用户）
- bob/123456（普通用户）
- 多篇文章，包含锁定/发布状态演示
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
from apps.articles.models import Article  # noqa: E402

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


def ensure_article(author, title, content, is_published=False, is_locked=False):
    obj = Article.objects.filter(author=author, title=title).first()
    if obj:
        # 同名文章存在时，更新状态字段以保证演示一致
        obj.content = content
        obj.is_published = is_published
        obj.is_locked = is_locked
        obj.save(update_fields=["content", "is_published", "is_locked"])
        return obj

    return Article.objects.create(
        author=author,
        title=title,
        content=content,
        is_published=is_published,
        is_locked=is_locked,
    )


def main():
    admin = ensure_user("admin", "admin123456", is_superuser=True, is_staff=True)
    alice = ensure_user("alice", "123456")
    bob = ensure_user("bob", "123456")

    ensure_article(alice, "Alice 的草稿", "alice draft", is_published=False, is_locked=False)
    ensure_article(alice, "Alice 的已发布", "alice published", is_published=True, is_locked=False)
    ensure_article(bob, "Bob 的锁定文章", "bob locked", is_published=True, is_locked=True)

    print("[init_data] users/articles ready")


if __name__ == "__main__":
    main()