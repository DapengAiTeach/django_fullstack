# movies/urls.py
from django.urls import path
from movies import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movie_list, name="movie_list"),
    path("movies/new/", views.movie_create, name="movie_create"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
]