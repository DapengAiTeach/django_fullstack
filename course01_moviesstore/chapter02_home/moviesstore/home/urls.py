from django.urls import path
from . import views

# 名称空间
app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
