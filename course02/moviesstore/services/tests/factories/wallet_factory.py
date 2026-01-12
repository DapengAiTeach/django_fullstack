# services/tests/factories/wallet_factory.py
from __future__ import annotations

from django.db import transaction

from apps.wallet.models import Wallet, CoinTransaction
from services.domain.wallet_service import WalletService


def _pick_tx_type(prefer: str = "INIT") -> str:
    """
    从 CoinTransaction 的枚举/choices 中选一个可用的 tx_type，避免枚举命名不一致导致测试失败。
    优先使用 prefer（例如 INIT / PURCHASE / RENEW），不存在则回退到任意一个可用值。
    """
    tx_enum = getattr(CoinTransaction, "TxType", None)
    if tx_enum and hasattr(tx_enum, prefer):
        return getattr(tx_enum, prefer)

    # Django TextChoices: choices 形如 [(value, label), ...]
    field = CoinTransaction._meta.get_field("type")
    if getattr(field, "choices", None):
        return field.choices[0][0]

    # 再兜底：字段没有 choices 的情况（极少），直接用字符串
    return prefer


def create_wallet(
    *,
    user,
    balance: int = 0,
) -> Wallet:
    """
    创建钱包（测试工厂）

    设计原则：
    - 只用于准备“初始状态”
    - 余额的变更尽量通过 WalletService.credit / debit（包含审计流水）
    - 如果你的业务要求“初始化余额也必须有流水”，则使用 credit 来补齐余额
    """
    if not user:
        raise ValueError("user 不能为空")

    wallet, _ = Wallet.objects.get_or_create(
        user=user,
        defaults={"balance": 0},
    )

    # 目标余额与当前余额不同，则通过 WalletService.credit/debit 调整到目标值
    # 这样保证余额变化带有 CoinTransaction 流水，符合你的业务审计要求
    target = int(balance)
    current = int(wallet.balance)

    if target == current:
        return wallet

    # 选择一个在你项目中真实存在的 tx_type
    tx_type = _pick_tx_type("INIT")

    if target > current:
        WalletService.credit(
            user=user,
            amount=target - current,
            tx_type=tx_type,
            ref_type="TEST_INIT",
            ref_id=wallet.id,
            remark="测试初始化钱包余额",
        )
    else:
        # 若目标余额小于当前余额：用 debit 调整（一般测试不太用到，但做完整）
        WalletService.debit(
            user=user,
            amount=current - target,
            tx_type=tx_type,
            ref_type="TEST_INIT",
            ref_id=wallet.id,
            remark="测试初始化钱包余额（扣减）",
        )

    return Wallet.objects.get(user=user)


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

    注意：
    - 仅限测试使用
    - 会删除该用户所有 CoinTransaction（确保干净）
    """
    Wallet.objects.filter(user=user).delete()
    CoinTransaction.objects.filter(user=user).delete()
    return create_wallet(user=user, balance=balance)
