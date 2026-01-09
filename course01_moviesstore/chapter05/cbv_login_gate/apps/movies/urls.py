from django.urls import path
from apps.movies import views

app_name = "movies"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("vip/", views.VipCBVView.as_view(), name="vip_cbv"),
    path("mro/", views.MROExplainView.as_view(), name="mro"),
    path("debug/", views.DebugView.as_view(), name="debug"),
]