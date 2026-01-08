# movies/admin.py
from django.contrib import admin
from .models import Director, Tag, Movie, Review


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "created_at")
    list_filter = ("director", "tags")
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "nickname", "score", "created_at")
    search_fields = ("movie__title", "nickname", "content")
