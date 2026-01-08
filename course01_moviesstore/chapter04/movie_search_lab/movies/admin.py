from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "rating", "is_hot", "created_at")
    list_filter = ("category", "is_hot")
    search_fields = ("title", "summary")
