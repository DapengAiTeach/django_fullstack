from django.db import models
from django.conf import settings


class Wallet(models.Model):
    """
    用户钱包表（余额快照）
    - 一对一绑定用户
    - balance 表示当前可用金币数量
    - 禁止后台直接改 balance（必须通过“管理员充值/扣减”写流水并更新）
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    balance = models.BigIntegerField(
        default=0,
        verbose_name="金币余额",
        help_text="当前可用金币数量，单位：个",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "wallet"
        verbose_name = "钱包"
        verbose_name_plural = "钱包"

    def __str__(self) -> str:
        return f"{self.user}（余额：{self.balance}）"


class CoinTransaction(models.Model):
    """
    金币流水表（账本）
    - 记录每一次金币变动，不允许修改或删除
    - 任何导致余额变化的行为，都必须写一条流水
    - 管理员充值/扣减同样写流水（可审计）
    """

    class TxType(models.TextChoices):
        RECHARGE = "RECHARGE", "充值入账（支付）"
        PURCHASE = "PURCHASE", "购买扣减"
        RENEW = "RENEW", "会员续费扣减"
        ADMIN_RECHARGE = "ADMIN_RECHARGE", "管理员充值"
        ADMIN_DEDUCT = "ADMIN_DEDUCT", "管理员扣减"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
        related_name="coin_transactions",
    )

    # 操作人（管理员）。支付回调等系统入账可以为空
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="操作人",
        related_name="coin_operator_transactions",
        help_text="管理员操作时记录管理员账号；系统自动流水可为空",
    )

    change_amount = models.BigIntegerField(
        verbose_name="变动数量",
        help_text="正数表示增加，负数表示减少",
    )
    balance_after = models.BigIntegerField(
        verbose_name="变动后余额",
    )
    type = models.CharField(
        max_length=30,
        choices=TxType.choices,
        verbose_name="流水类型",
    )

    # 关联业务（用于追溯）
    ref_type = models.CharField(
        max_length=30,
        verbose_name="关联业务类型",
        help_text="如 RECHARGE_ORDER / PURCHASE_ORDER / ADMIN",
    )
    ref_id = models.BigIntegerField(
        verbose_name="关联业务ID",
        help_text="可记录订单ID；管理员操作可记录管理员ID",
    )

    remark = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="备注",
        help_text="管理员操作必填：充值/扣减原因",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "coin_transaction"
        verbose_name = "金币流水"
        verbose_name_plural = "金币流水"
        indexes = [
            models.Index(fields=["user", "created_at"], name="idx_tx_user_time"),
            models.Index(fields=["ref_type", "ref_id"], name="idx_tx_ref"),
        ]

    def __str__(self) -> str:
        return f"{self.user} {self.type} {self.change_amount}（余额：{self.balance_after}）"