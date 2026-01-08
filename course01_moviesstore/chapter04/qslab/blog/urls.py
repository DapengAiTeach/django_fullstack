from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("seed/", views.seed, name="seed"),  # 一键造数据
    path("lab/", views.query_lab, name="lab"),  # QuerySet 实验室
]
