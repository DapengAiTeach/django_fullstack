# services/tests/factories/wallet_factory.py
from __future__ import annotations

from typing import Optional

from django.db import transaction

from apps.wallet.models import Wallet, CoinTransaction
from services.domain.wallet_service import WalletService


def create_wallet(
    *,
    user,
    balance: int = 0,
) -> Wallet:
    """
    创建钱包（测试工厂）

    设计原则：
    - 测试中不直接操作 Wallet.balance 的业务含义
    - 仅用于准备“初始状态”
    - 后续余额变化必须通过 WalletService.credit / debit

    参数：
    - user: 用户对象（必传）
    - balance: 初始余额（可为 0）
    """
    if not user:
        raise ValueError("user 不能为空")

    wallet, created = Wallet.objects.get_or_create(
        user=user,
        defaults={"balance": 0},
    )

    # 如果需要非 0 初始余额，使用 WalletService.credit 补齐
    if balance > 0 and wallet.balance != balance:
        WalletService.credit(
            user=user,
            amount=balance - wallet.balance,
            tx_type=CoinTransaction.TxType.INIT,
            ref_type="TEST_INIT",
            ref_id=wallet.id,
            remark="测试初始化钱包余额",
        )

    # 如果 balance == 0 但数据库中已有余额（极少见），强制清零
    if balance == 0 and wallet.balance != 0:
        # 直接修正，仅用于测试环境
        wallet.balance = 0
        wallet.save(update_fields=["balance"])

        CoinTransaction.objects.filter(
            user=user,
            ref_type="TEST_INIT",
        ).delete()

    return wallet


def create_wallet_with_balance(
    *,
    user,
    balance: int,
) -> Wallet:
    """
    语义化别名：创建带初始余额的钱包
    """
    return create_wallet(user=user, balance=balance)


@transaction.atomic
def reset_wallet(
    *,
    user,
    balance: int = 0,
):
    """
    重置用户钱包（测试辅助工具）

    使用场景：
    - 多个测试用例复用同一 user
    - 需要确保钱包状态干净

    注意：
    - 仅限测试使用
    - 会删除该用户所有 CoinTransaction
    """
    Wallet.objects.filter(user=user).delete()
    CoinTransaction.objects.filter(user=user).delete()

    return create_wallet(user=user, balance=balance)