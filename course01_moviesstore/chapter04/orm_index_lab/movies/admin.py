# movies/admin.py
from django.contrib import admin
from .models import Director, Movie, MovieSKU


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class MovieSKUInline(admin.TabularInline):
    model = MovieSKU
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "category", "is_active", "rating", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("title", "director__name")
    ordering = ("-created_at",)
    inlines = [MovieSKUInline]


@admin.register(MovieSKU)
class MovieSKUAdmin(admin.ModelAdmin):
    list_display = ("movie", "edition", "price")
    search_fields = ("movie__title", "edition")
