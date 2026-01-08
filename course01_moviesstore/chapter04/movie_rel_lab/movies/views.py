# movies/views.py
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from .models import Movie, Order, OrderItem
from .forms import OrderCreateForm


def home(request):
    return render(request, "movies/home.html")


def movie_list(request):
    movies = Movie.objects.select_related("director").order_by("-created_at")
    return render(request, "movies/movie_list.html", {"movies": movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.select_related("director"), pk=pk)

    # 反向关系演示：导演 -> 电影（一对多的反向查询）
    director_other_movies = movie.director.movies.exclude(pk=movie.pk)[:6]

    return render(
        request,
        "movies/movie_detail.html",
        {"movie": movie, "director_other_movies": director_other_movies},
    )


@login_required
def order_create(request):
    """
    多对多（带额外字段）写入演示：
    - Order 创建
    - OrderItem 批量写入
    """
    form = OrderCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        movies = form.cleaned_data["movie_ids"]
        quantity = form.cleaned_data["quantity"]

        with transaction.atomic():
            order = Order.objects.create(user=request.user)

            items = []
            for m in movies:
                items.append(
                    OrderItem(
                        order=order,
                        movie=m,
                        quantity=quantity,
                        deal_price=m.price,  # 成交价：此处取当前价格（演示快照）
                    )
                )
            OrderItem.objects.bulk_create(items)

        return redirect("movies:movie_list")

    return render(request, "movies/order_create.html", {"form": form})
