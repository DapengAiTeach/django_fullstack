from django.contrib import admin
from apps.movies.models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]

    class Media:
        """
        注入自定义 Admin CSS / JS
        """
        css = {
            "all": ("admin_ext/css/admin_theme.css",)
        }
        js = ("admin_ext/js/admin_enhance.js",)