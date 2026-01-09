from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.movies.models import Movie

class DefaultPermissionTests(TestCase):
    def test_default_permissions_exist_and_naming(self):
        ct = ContentType.objects.get_for_model(Movie)

        # 默认权限 codename 规则：动作_模型名小写
        expected = {"add_movie", "change_movie", "delete_movie", "view_movie"}

        perms = Permission.objects.filter(content_type=ct, codename__in=expected)
        self.assertEqual(perms.count(), 4)

        # app_label.codename 规则：movies.add_movie
        keys = {f"{p.content_type.app_label}.{p.codename}" for p in perms}
        self.assertTrue("movies.add_movie" in keys)
        self.assertTrue("movies.change_movie" in keys)
        self.assertTrue("movies.delete_movie" in keys)
        self.assertTrue("movies.view_movie" in keys)