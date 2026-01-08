from django.urls import path
from movies import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("directors/", views.director_list, name="director_list"),
    path("directors/<int:pk>/", views.director_detail, name="director_detail"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
]
