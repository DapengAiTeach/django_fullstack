from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # API 统一挂在 /api/
    path("api/", include("apps.movies.urls")),
]