# movies/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, MoviePhoto

class MoviePhotoInline(admin.TabularInline):
    model = MoviePhoto
    extra = 0

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "cover_preview", "created_at")
    search_fields = ("title",)
    inlines = [MoviePhotoInline]

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.cover.url)
        return "-"
    cover_preview.short_description = "封面预览"

@admin.register(MoviePhoto)
class MoviePhotoAdmin(admin.ModelAdmin):
    list_display = ("movie", "image_preview", "caption", "created_at")
    search_fields = ("movie__title", "caption")

    def image_preview(self, obj):
        return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
    image_preview.short_description = "剧照预览"