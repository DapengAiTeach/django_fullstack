from django.contrib import admin
from apps.accounts.admin_sites import ops_site
from apps.movies.models import Movie, Genre

@admin.register(Movie, site=ops_site)
class OpsMovieAdmin(admin.ModelAdmin):
    """
    运营后台：更关心“上架状态、价格、标题”，字段更少更清爽。
    """
    list_display = ["id", "title", "price", "is_published", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title"]
    ordering = ["-created_at"]


@admin.register(Genre, site=ops_site)
class OpsGenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]