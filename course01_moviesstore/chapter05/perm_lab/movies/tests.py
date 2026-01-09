from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from movies.models import Movie

User = get_user_model()

class PermissionMergeTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="alice123456")

        self.editor = Group.objects.create(name="Editor")

        ct = ContentType.objects.get_for_model(Movie)

        self.publish_movie = Permission.objects.get(content_type=ct, codename="publish_movie")
        self.export_movie = Permission.objects.get(content_type=ct, codename="export_movie")
        self.view_movie = Permission.objects.get(content_type=ct, codename="view_movie")

        # 角色给 publish/view
        self.editor.permissions.set([self.publish_movie, self.view_movie])

        # alice 加入角色
        self.alice.groups.add(self.editor)

        # alice 单独赋 export
        self.alice.user_permissions.add(self.export_movie)

    def test_group_permission_works(self):
        self.assertTrue(self.alice.has_perm("movies.publish_movie"))  # 来自 Group

    def test_user_permission_works(self):
        self.assertTrue(self.alice.has_perm("movies.export_movie"))   # 来自 user_permissions

    def test_merge_works(self):
        self.assertTrue(self.alice.has_perm("movies.view_movie"))     # 来自 Group
        self.assertTrue(self.alice.has_perm("movies.export_movie"))   # 来自 user_permissions