from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.movies"  # ✅ 必须是 apps.movies
    verbose_name = "电影管理"

    def ready(self):
        # ✅ 确保 ops_admin 被加载，从而注册到 ops_site
        from . import ops_admin  # noqa: F401
