from django.urls import path
from movies import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movie_feed, name="movie_feed"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
]