from django.urls import path
from apps.movies import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
]