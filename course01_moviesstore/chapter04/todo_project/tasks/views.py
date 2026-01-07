from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Task
from .forms import TaskForm


def task_list(request):
    """
    Read 演示区：all / filter / exclude / first / last / get（通过详情/编辑触发）
    页面功能：
    - 列表展示
    - 关键词搜索（title/description）
    - 过滤：未完成 / 已完成
    - 展示 first/last 示例
    """

    qs = Task.objects.all()

    keyword = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if keyword:
        # filter + Q：WHERE title LIKE ... OR description LIKE ...
        qs = qs.filter(Q(title__icontains=keyword) |
                       Q(description__icontains=keyword))

    if status == "todo":
        # filter：WHERE is_done = 0
        qs = qs.filter(is_done=False)
    elif status == "done":
        # filter：WHERE is_done = 1
        qs = qs.filter(is_done=True)

    # exclude：把低优先级排除掉（演示用）
    hide_low = request.GET.get("hide_low", "") == "1"
    if hide_low:
        # WHERE priority != 1
        qs = qs.exclude(priority=1)

    first_task = qs.first()  # ORDER BY ... LIMIT 1
    last_task = qs.last()  # 需要排序字段配合（Meta.ordering）

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": qs,
            "keyword": keyword,
            "status": status,
            "hide_low": hide_low,
            "first_task": first_task,
            "last_task": last_task,
        },
    )


def task_create(request):
    """
    Create 演示区：
    - Model.objects.create()
    - Model.save()

    页面用 ModelForm 保存（更贴近真实项目）。
    额外提供一个“快速创建”示例，演示 objects.create()
    """

    if request.method == "POST":
        # 1) 常规方式：ModelForm -> save() -> 内部会调用模型 save()
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:list")
    else:
        form = TaskForm()

    # 2) 演示 Model.objects.create()（通常用于脚本/批量导入/后台任务）
    if request.GET.get("quick") == "1":
        Task.objects.create(
            title="（示例）使用 objects.create() 创建的任务",
            description="这是用 ORM 一句话插入记录：INSERT INTO ...",
            priority=2,
            is_done=False,
        )
        return redirect("tasks:list")

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "mode": "create"},
    )


def task_edit(request, pk: int):
    """
    Update 演示区（实例修改 + save）：
    - get() / get_object_or_404：SELECT ... WHERE id=pk LIMIT 1
    - 实例修改：obj.title=...
    - obj.save()：UPDATE ... WHERE id=pk
    """

    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # ModelForm 会把更改写回实例，并调用 task.save()
            form.save()
            return redirect("tasks:list")
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "mode": "edit", "task": task},
    )


def task_bulk_done(request):
    """
    Update 演示区（QuerySet.update 批量更新）：
    - qs.update(...) 会生成：UPDATE ... SET is_done=1 WHERE ...
    - 注意：update() 不会触发模型 save()、也不会触发 signals
    """

    if request.method == "POST":
        ids = request.POST.getlist("ids")
        if ids:
            Task.objects.filter(id__in=ids).update(is_done=True)
        return redirect("tasks:list")

    return redirect("tasks:list")


def task_delete(request, pk: int):
    """
    Delete 演示区：
    - obj.delete()：DELETE FROM ... WHERE id=pk
    """

    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("tasks:list")

    # GET 进来显示确认页（更符合 UX）
    return render(
        request,
        "tasks/task_confirm_delete.html",
        {"task": task},
    )
