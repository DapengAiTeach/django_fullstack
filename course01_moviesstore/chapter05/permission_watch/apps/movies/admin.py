from django.contrib import admin
from apps.movies.models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year")
    search_fields = ("title",)