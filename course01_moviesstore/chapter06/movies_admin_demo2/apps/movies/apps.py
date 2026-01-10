from django.apps import AppConfig

class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.movies"  # ✅ 必须是 apps.movies
    verbose_name = "电影管理"