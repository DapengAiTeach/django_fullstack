# shop/views.py
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseBadRequest

from .models import Product, Order, OrderItem
from .forms import OrderCreateForm, PayCallbackForm


def home(request):
    return render(request, "shop/home.html")


def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})


def order_create(request, product_id):
    """
    ✅ 正确工程做法：下单 + 扣库存 必须在一个事务里
    并且要处理并发写：
    - select_for_update() 行锁（事务中生效）
    - F 表达式原子扣减，避免读-改-写竞争
    """
    product = get_object_or_404(Product, pk=product_id)
    form = OrderCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        qty = form.cleaned_data["quantity"]

        with transaction.atomic():
            # 1) 行锁：锁住这一行库存（直到事务结束）
            locked = Product.objects.select_for_update().get(pk=product.id)

            # 2) 库存校验：在锁内判断才可靠
            if locked.stock < qty:
                # 触发回滚：抛异常或返回（这里返回也行，但不要修改数据）
                return render(
                    request,
                    "shop/order_result.html",
                    {"ok": False, "msg": f"库存不足：当前库存 {locked.stock}，你要买 {qty}"},
                )

            # 3) 原子扣库存：避免并发读-改-写
            Product.objects.filter(pk=locked.id).update(stock=F("stock") - qty)

            # 4) 创建订单 & 订单项（同一事务）
            order = Order.objects.create(status=Order.Status.CREATED)
            OrderItem.objects.create(
                order=order,
                product=locked,
                quantity=qty,
                deal_price=locked.price,  # 价格快照
            )

        return redirect("shop:pay_success", order_id=order.id)

    return render(request, "shop/order_create.html", {"product": product, "form": form})


def pay_success(request, order_id):
    """
    支付成功回调（模拟）：
    - 必须幂等：同一个 order_id 多次回调，不应重复改状态/重复扣库存
    - 这里只改状态，不动库存（库存已在下单时扣了）
    """
    order = get_object_or_404(Order.objects.select_related("item__product"), pk=order_id)
    form = PayCallbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        payment_no = form.cleaned_data["payment_no"]

        with transaction.atomic():
            # 再次锁住订单，避免并发回调
            locked_order = Order.objects.select_for_update().get(pk=order.id)

            # ✅ 幂等：如果已支付，直接返回成功
            if locked_order.status == Order.Status.PAID:
                return render(request, "shop/pay_result.html", {"ok": True, "order": locked_order, "msg": "已支付（幂等命中）"})

            # ✅ 只有 CREATED 才允许变为 PAID
            if locked_order.status != Order.Status.CREATED:
                return render(request, "shop/pay_result.html", {"ok": False, "order": locked_order, "msg": "订单状态异常，无法支付"})

            locked_order.status = Order.Status.PAID
            locked_order.payment_no = payment_no
            locked_order.save(update_fields=["status", "payment_no"])

        return render(request, "shop/pay_result.html", {"ok": True, "order": locked_order, "msg": "支付成功（状态已更新）"})

    # 默认生成一个随机支付单号，方便测试
    if request.method == "GET" and not order.payment_no:
        form.initial = {"payment_no": f"PAY{random.randint(100000, 999999)}"}

    return render(request, "shop/pay_success.html", {"order": order, "form": form})


def pay_fail(request, order_id):
    """
    支付失败/取消回调（模拟）：
    - 必须事务：订单状态更新 + 回滚库存 要么都成功，要么都失败
    - 幂等：如果已经取消或已支付，不应重复回滚库存
    """
    order = get_object_or_404(Order.objects.select_related("item__product"), pk=order_id)

    with transaction.atomic():
        locked_order = Order.objects.select_for_update().get(pk=order.id)

        if locked_order.status == Order.Status.CANCELED:
            return render(request, "shop/pay_result.html", {"ok": True, "order": locked_order, "msg": "已取消（幂等命中）"})

        if locked_order.status == Order.Status.PAID:
            return render(request, "shop/pay_result.html", {"ok": False, "order": locked_order, "msg": "已支付订单不能取消"})

        # CREATED => CANCELED，并回滚库存
        item = locked_order.item
        Product.objects.filter(pk=item.product_id).update(stock=F("stock") + item.quantity)

        locked_order.status = Order.Status.CANCELED
        locked_order.save(update_fields=["status"])

    return render(request, "shop/pay_result.html", {"ok": True, "order": locked_order, "msg": "取消成功（库存已回滚）"})


def concurrency_demo(request, product_id):
    """
    并发演示入口页：
    - 展示“错误写法”和“正确写法”差异
    """
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shop/concurrency_demo.html", {"product": product})