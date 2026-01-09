from django.urls import path
from apps.movies import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("session/", views.session_debug, name="session_debug"),
]