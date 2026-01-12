from django.contrib import admin
from .models import UserIdentity


@admin.register(UserIdentity)
class UserIdentityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "identity_type",
        "identifier",
        "is_primary",
        "is_verified",
        "created_at",
    )
    list_filter = ("identity_type", "is_verified")
    search_fields = ("identifier",)