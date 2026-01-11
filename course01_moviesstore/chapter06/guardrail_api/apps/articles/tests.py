from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from apps.articles.models import Article

User = get_user_model()


class PermissionSystemTests(APITestCase):
    """
    覆盖：
    - IsAuthenticated：未登录访问被拒绝
    - DjangoModelPermissions：按 add/change/delete/view 进行接口级控制
    - 对象级权限：IsOwnerOrAdmin + IsNotLockedOrAdmin
    - IsAdminUser：lock/unlock 仅管理员
    """

    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="admin123456")
        self.alice = User.objects.create_user(username="alice", password="123456")
        self.bob = User.objects.create_user(username="bob", password="123456")

        self.alice_article = Article.objects.create(author=self.alice, title="A1", content="c1", is_published=False, is_locked=False)
        self.bob_locked = Article.objects.create(author=self.bob, title="B1", content="c2", is_published=True, is_locked=True)

        # 给普通用户分配 model perms（DjangoModelPermissions 会检查这些权限）
        # 默认 create_user 不会自动赋予 perms，这里明确赋权以符合接口设计
        # 仅给 alice 赋：view/add/change/delete Article（演示用途）
        from django.contrib.auth.models import Permission
        perms = Permission.objects.filter(codename__in=["view_article", "add_article", "change_article", "delete_article"])
        self.alice.user_permissions.add(*perms)

        self.bob.user_permissions.add(*perms)

    def test_unauthenticated_should_be_denied(self):
        r = self.client.get("/api/articles/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r.data["code"], 40301)

    def test_list_should_return_only_self_for_normal_user(self):
        self.client.login(username="alice", password="123456")  # SessionAuthentication
        r = self.client.get("/api/articles/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        data = r.data["data"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["author_id"], self.alice.id)

    def test_owner_can_update_but_not_locked(self):
        self.client.login(username="alice", password="123456")

        # alice 更新自己的文章允许
        r = self.client.patch(f"/api/articles/{self.alice_article.id}/", data={"title": "A1-updated"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)

        # alice 尝试修改 bob 的锁定文章，必须拒绝（对象级权限）
        r = self.client.patch(f"/api/articles/{self.bob_locked.id}/", data={"title": "hack"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r.data["code"], 40301)

    def test_admin_can_lock_unlock(self):
        self.client.login(username="admin", password="admin123456")

        r = self.client.post(f"/api/articles/{self.alice_article.id}/lock/", data={}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        self.assertTrue(r.data["data"]["is_locked"])

        r = self.client.post(f"/api/articles/{self.alice_article.id}/unlock/", data={}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        self.assertFalse(r.data["data"]["is_locked"])

    def test_publish_requires_owner_or_admin(self):
        self.client.login(username="alice", password="123456")

        # alice 发布自己的文章 OK
        r = self.client.post(f"/api/articles/{self.alice_article.id}/publish/", data={}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["code"], 0)
        self.assertTrue(r.data["data"]["is_published"])

        # alice 发布 bob 的文章，必须拒绝
        r = self.client.post(f"/api/articles/{self.bob_locked.id}/publish/", data={}, format="json")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(r.data["code"], 40301)