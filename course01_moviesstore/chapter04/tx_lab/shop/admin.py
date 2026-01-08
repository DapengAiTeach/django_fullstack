# shop/admin.py
from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "created_at")
    search_fields = ("name",)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "payment_no", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]