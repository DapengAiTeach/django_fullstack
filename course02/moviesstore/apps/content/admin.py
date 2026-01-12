from django.contrib import admin
from .models import Movie, MovieDetail, MovieAsset
from .forms import MovieAdminForm


class MovieDetailInline(admin.StackedInline):
    model = MovieDetail
    extra = 0


class MovieAssetInline(admin.TabularInline):
    model = MovieAsset
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm

    list_display = (
        "id",
        "title",
        "access_type",
        "price_coin",
        "status",
        "published_at",
    )
    list_filter = ("status", "access_type")
    search_fields = ("title",)

    inlines = [
        MovieDetailInline,
        MovieAssetInline,
    ]