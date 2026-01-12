from django.contrib import admin
from .models import DownloadToken, DownloadDailyQuota


@admin.register(DownloadToken)
class DownloadTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "device_id", "expires_at", "created_at")
    list_filter = ("expires_at",)
    search_fields = ("user__username", "movie__title", "device_id")
    readonly_fields = ("user", "movie", "device_id", "expires_at", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DownloadDailyQuota)
class DownloadDailyQuotaAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "date", "count")
    list_filter = ("date",)
    search_fields = ("user__username", "movie__title")
    readonly_fields = ("user", "movie", "date", "count")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
