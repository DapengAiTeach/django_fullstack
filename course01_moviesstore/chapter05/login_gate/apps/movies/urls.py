from django.urls import path
from apps.movies import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("vip/", views.vip, name="vip"),                 # ✅ login_required 保护页
    path("next-debug/", views.next_debug, name="next_debug"),
]