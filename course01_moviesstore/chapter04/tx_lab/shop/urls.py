from django.urls import path
from shop import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),

    path("orders/new/<int:product_id>/", views.order_create, name="order_create"),

    # 模拟支付回调：成功/失败
    path("pay/success/<int:order_id>/", views.pay_success, name="pay_success"),
    path("pay/fail/<int:order_id>/", views.pay_fail, name="pay_fail"),

    # 并发演示入口：不加锁 vs 加锁
    path("demo/concurrency/<int:product_id>/", views.concurrency_demo, name="concurrency_demo"),
]