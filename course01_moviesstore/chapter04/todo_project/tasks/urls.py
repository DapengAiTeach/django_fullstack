from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="list"),
    path("create/", views.task_create, name="create"),
    path("<int:pk>/edit/", views.task_edit, name="edit"),
    path("<int:pk>/delete/", views.task_delete, name="delete"),

    # 用来演示 QuerySet.update() 的“批量更新”
    path("bulk/done/", views.task_bulk_done, name="bulk_done"),
]
