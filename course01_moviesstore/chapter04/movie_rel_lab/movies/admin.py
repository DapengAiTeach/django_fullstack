# movies/admin.py
from django.contrib import admin
from .models import Director, Movie, Order, OrderItem


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "price", "created_at")
    list_filter = ("director",)
    search_fields = ("title",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    inlines = [OrderItemInline]


