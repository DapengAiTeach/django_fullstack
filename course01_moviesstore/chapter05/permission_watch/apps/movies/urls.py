from django.urls import path
from apps.movies import views

app_name = "movies"

urlpatterns = [
    path("", views.perm_dashboard, name="perm_dashboard"),
    path("api/default-perms/", views.default_perms_api, name="default_perms_api"),
]