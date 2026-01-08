from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages

from .models import Movie, MoviePhoto
from .forms import MovieCreateForm


def home(request):
    """
    首页：入口页
    """
    return render(request, "movies/home.html")


def movie_list(request):
    """
    电影列表：
    - 展示封面（movie.cover.url）
    - 点击进入详情页
    """
    movies = Movie.objects.all()  # Movie.Meta.ordering 默认 -created_at
    return render(request, "movies/movie_list.html", {"movies": movies})


def movie_detail(request, pk):
    """
    电影详情：
    - 展示封面
    - 展示多张剧照（反向：movie.photos.all）
    """
    movie = get_object_or_404(
        Movie.objects.prefetch_related("photos"),
        pk=pk
    )
    return render(request, "movies/movie_detail.html", {"movie": movie})


def movie_create(request):
    """
    创建电影 + 上传媒体文件（封面单图 + 剧照多图）

    Django 5 注意点：
    - 多文件上传不要用 Form 的 multiple FileInput（会 ValueError）
    - 模板用 <input type="file" name="photos" multiple>
    - 视图用 request.FILES.getlist("photos")

    一致性：
    - 用 transaction.atomic() 确保：电影创建 + 剧照记录创建要么一起成功，要么一起失败
    """
    form = MovieCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            with transaction.atomic():
                movie = form.save()  # cover 文件会自动保存到 MEDIA_ROOT

                # ✅ 多文件：从请求中取出同名字段的所有文件
                files = request.FILES.getlist("photos")

                # ✅ 稳妥写法：逐条 create（能触发完整保存流程）
                for f in files:
                    # 这里不强制校验类型/大小，你想要我可以再补一版带校验的
                    MoviePhoto.objects.create(movie=movie, image=f)

            messages.success(request, "上传成功：电影与剧照已保存！")
            return redirect("movies:movie_detail", pk=movie.pk)

        # 表单无效：给一个友好提示
        messages.error(request, "提交失败：请检查表单内容（标题/图片）是否正确。")

    return render(request, "movies/movie_create.html", {"form": form})
