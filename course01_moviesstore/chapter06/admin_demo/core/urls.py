from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include
from django.views import View
from django.shortcuts import redirect


class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Django 5 admin logout is POST-only; provide a GET-friendly redirect.
        logout(request)
        return redirect("admin:login")

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("admin:login")

urlpatterns = [
    path("admin/logout/", AdminLogoutView.as_view(), name="admin_logout"),
    path("admin/", admin.site.urls),
    path("", include("apps.home.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
