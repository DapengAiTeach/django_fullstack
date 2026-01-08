# movies/admin.py
from django.contrib import admin
from movies.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year", "owner", "created_at")
    search_fields = ("title",)
    list_filter = ("year", "created_at")
    ordering = ("-created_at",)

    # ✅ 可选：让普通后台用户只能看到自己的数据（示范：权限与 ORM 的关系）
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
