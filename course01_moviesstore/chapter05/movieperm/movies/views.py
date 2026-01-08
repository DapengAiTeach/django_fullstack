# movies/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from movies.forms import LoginForm, MovieForm
from movies.models import Movie

# ---------- 认证：登录 / 退出（Authentication） ----------

def user_login(request):
    """
    Authentication：你是谁？
    - authenticate: 校验用户名密码
    - login: 写入 session，后续 request.user 变为登录用户
    """
    if request.user.is_authenticated:
        return redirect("movies:movie_list")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            messages.success(request, "登录成功！")
            # 支持 next 跳转
            next_url = request.GET.get("next") or "movies:movie_list"
            return redirect(next_url)
        messages.error(request, "用户名或密码错误")

    return render(request, "auth/login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.info(request, "你已退出登录")
    return redirect("movies:movie_list")


# ---------- 业务：列表与详情（任何人可看） ----------

def movie_list(request):
    movies = Movie.objects.select_related("owner").all()
    return render(request, "movies/movie_list.html", {"movies": movies})

def movie_detail(request, pk: int):
    movie = get_object_or_404(Movie.objects.select_related("owner"), pk=pk)
    return render(request, "movies/movie_detail.html", {"movie": movie})


# ---------- 授权：新增/编辑/删除（Authorization） ----------

@login_required
@permission_required("movies.add_movie", raise_exception=True)
def movie_create(request):
    """
    Authorization：你能做什么？
    - permission_required 会调用 user.has_perm("movies.add_movie")
    """
    form = MovieForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user  # ✅ 对象归属
        obj.save()
        messages.success(request, "新增成功！")
        return redirect("movies:movie_detail", pk=obj.pk)

    return render(request, "movies/movie_form.html", {"form": form, "mode": "create"})


@login_required
@permission_required("movies.change_movie", raise_exception=True)
def movie_update(request, pk: int):
    """
    视图层授权（change_movie） + ORM 数据范围（只能改自己的）
    """
    movie = get_object_or_404(Movie, pk=pk)

    # ✅ 对象级规则（示范：权限系统与 ORM 的配合）
    # 即使拥有 change_movie 权限，也不允许改别人的数据（除非超级用户）
    if not request.user.is_superuser and movie.owner_id != request.user.id:
        # 也可以直接返回 403，这里演示“隐藏存在性”用 404
        raise Http404("你无权编辑该资源")

    form = MovieForm(request.POST or None, instance=movie)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "保存成功！")
        return redirect("movies:movie_detail", pk=movie.pk)

    return render(request, "movies/movie_form.html", {"form": form, "mode": "edit"})


@login_required
@permission_required("movies.delete_movie", raise_exception=True)
def movie_delete(request, pk: int):
    movie = get_object_or_404(Movie, pk=pk)

    if not request.user.is_superuser and movie.owner_id != request.user.id:
        raise Http404("你无权删除该资源")

    if request.method == "POST":
        movie.delete()
        messages.success(request, "删除成功！")
        return redirect("movies:movie_list")

    return render(request, "movies/movie_confirm_delete.html", {"movie": movie})