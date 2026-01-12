from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem, PurchaseLicense


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("movie", "price_coin", "created_at")


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_coin", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "user__email")
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ("user", "total_coin", "status", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PurchaseLicense)
class PurchaseLicenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")
    readonly_fields = ("user", "movie", "order_item", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
