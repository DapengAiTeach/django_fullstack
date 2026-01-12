from django.urls import path
from .views import health

app_name = "content"

urlpatterns = [
    path("health/", health),
]