from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "status", "start_at", "end_at")
    list_filter = ("plan", "status")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("user", "plan", "status", "start_at", "end_at", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False