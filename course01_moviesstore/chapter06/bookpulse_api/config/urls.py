from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # API 统一前缀
    path("api/", include("apps.reviews.urls")),
]