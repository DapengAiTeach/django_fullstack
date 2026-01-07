from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


# 显示所有任务
def task_list(request):
    tasks = Task.objects.all()
    return render(
        request,
        'tasks/task_list.html',
        {'tasks': tasks},
    )


# 创建新任务
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(
        request,
        'tasks/task_form.html',
        {'form': form},
    )
