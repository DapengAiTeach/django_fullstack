from django.apps import AppConfig


class CommonConfig(AppConfig):
    # 通用工具应用，用于存放模板标签与公共工具代码
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"
    verbose_name = "公共工具"
