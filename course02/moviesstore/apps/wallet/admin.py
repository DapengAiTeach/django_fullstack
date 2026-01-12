# apps/wallet/admin.py
from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Wallet, CoinTransaction
from .forms import AdminCoinAdjustForm


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    钱包后台管理：
    - 钱包只读
    - 提供“管理员充值 / 扣减”入口
    """

    list_display = ("id", "user", "balance", "updated_at", "adjust_link")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("user", "balance", "created_at", "updated_at")

    # ========= 关键点 1：adjust_link 必须是 WalletAdmin 的方法 =========
    def adjust_link(self, obj):
        url = reverse("admin:wallet_adjust", args=[obj.id])
        return format_html(
            '<a class="button" href="{}">充值 / 扣减</a>',
            url,
        )

    adjust_link.short_description = "金币调整"

    # ========= 关键点 2：权限控制 =========
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # ========= 自定义 URL =========
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:wallet_id>/adjust/",
                self.admin_site.admin_view(self.adjust_view),
                name="wallet_adjust",
            ),
        ]
        return custom_urls + urls

    # ========= 调整页面 =========
    def adjust_view(self, request, wallet_id: int):
        wallet = Wallet.objects.select_related("user").filter(id=wallet_id).first()
        if not wallet:
            messages.error(request, "钱包不存在")
            return redirect("admin:wallet_wallet_changelist")

        if request.method == "POST":
            form = AdminCoinAdjustForm(request.POST)
            if form.is_valid():
                try:
                    self._apply_adjust(
                        request=request,
                        wallet_id=wallet.id,
                        action=form.cleaned_data["action"],
                        amount=form.cleaned_data["amount"],
                        remark=form.cleaned_data["remark"],
                    )
                    messages.success(request, "金币调整成功")
                    return redirect("admin:wallet_wallet_change", wallet.id)
                except ValueError as e:
                    messages.error(request, str(e))
        else:
            form = AdminCoinAdjustForm()

        context = dict(
            self.admin_site.each_context(request),
            title="管理员金币调整",
            wallet=wallet,
            form=form,
        )
        return render(request, "admin/wallet/wallet/adjust.html", context)

    # ========= 核心事务逻辑 =========
    def _apply_adjust(self, request, wallet_id, action, amount, remark):
        if amount <= 0:
            raise ValueError("金币数量必须大于 0")

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=wallet_id)

            if action == AdminCoinAdjustForm.ACTION_RECHARGE:
                change_amount = amount
                tx_type = CoinTransaction.TxType.ADMIN_RECHARGE
            else:
                change_amount = -amount
                tx_type = CoinTransaction.TxType.ADMIN_DEDUCT
                if wallet.balance + change_amount < 0:
                    raise ValueError("余额不足，无法扣减")

            wallet.balance += change_amount
            wallet.updated_at = timezone.now()
            wallet.save(update_fields=["balance", "updated_at"])

            CoinTransaction.objects.create(
                user=wallet.user,
                operator=request.user,
                change_amount=change_amount,
                balance_after=wallet.balance,
                type=tx_type,
                ref_type="ADMIN",
                ref_id=request.user.id,
                remark=remark,
            )
