# services/tests/domain/test_wallet_service.py
from __future__ import annotations

"""
本测试文件用于验证：WalletService（钱包领域服务）的核心业务行为是否正确。

为什么要单独对 Service 层做单元测试？
- Service 层承载“业务规则 + 数据一致性 + 审计流水”，是后台管理端、Web端、App端共同依赖的核心。
- View/Serializer 可以变化，但 Service 的业务规则必须稳定、可回归、可审计。

本文件的测试目标（必须明确）：
1. credit（入账）
   - 钱包余额增加正确
   - 生成一条 CoinTransaction 流水
   - 流水审计字段（change_amount / balance_after / type / ref_type / ref_id 等）正确
2. debit（扣款）
   - 钱包余额扣减正确
   - 生成一条 CoinTransaction 流水
   - 审计字段正确
3. debit（余额不足）
   - 必须抛出 BalanceNotEnough
   - 钱包余额不变
   - 不应产生任何新流水（强一致原则：失败不落审计记录）
4. get_or_create
   - 用户无钱包时自动创建
   - 多次调用返回同一个钱包（幂等）

测试写作规范（后续你要求所有单元测试都遵循）：
- 每个测试函数必须包含：
  1) 测试目的（要验证什么业务规则）
  2) 测试前置（准备哪些数据）
  3) 测试步骤（调用什么 Service 方法）
  4) 断言点（为什么要这么断言）
- 断言不仅断结果（余额），还要断“审计痕迹”（流水字段），否则测试价值不足。
"""

from django.test import TestCase

from apps.wallet.models import Wallet, CoinTransaction
from services.common.exceptions import BalanceNotEnough
from services.domain.wallet_service import WalletService
from services.tests.factories.user_factory import create_user, create_admin
from services.tests.factories.wallet_factory import create_wallet_with_balance


def _pick_tx_type(prefer: str = "INIT") -> str:
    """
    测试辅助函数：选择一个“在当前项目中真实存在”的 CoinTransaction.type 值。

    背景：
    - 你的 CoinTransaction.type 往往是枚举（TextChoices 或 Enum）
    - 不同项目/阶段枚举命名可能不同（例如 INIT 可能不存在）
    - 如果测试里硬编码 CoinTransaction.TxType.INIT，会因枚举不存在而导致测试本身报错（不是业务失败）

    目标：
    - 在不改业务代码的前提下，让测试具备更强的“适配性”
    - 优先使用 prefer 指定的枚举值（如果存在）
    - 不存在则回退到模型字段 choices 的第一个合法值
    - 再不行则兜底返回字符串 prefer（字段不限制 choices 的情况下仍可写入）

    参数：
    - prefer: 首选的交易类型名称（例如 "INIT" / "PURCHASE" / "RENEW"）

    返回：
    - 可用于 CoinTransaction.type 的合法值
    """
    # 1) 如果你的模型定义了 CoinTransaction.TxType（通常是 Enum / TextChoices）
    tx_enum = getattr(CoinTransaction, "TxType", None)
    if tx_enum and hasattr(tx_enum, prefer):
        return getattr(tx_enum, prefer)

    # 2) 尝试从字段 choices 取第一个合法值（最通用）
    # Django TextChoices 通常在字段元信息里以 choices 形式存在
    field = CoinTransaction._meta.get_field("type")
    if getattr(field, "choices", None):
        return field.choices[0][0]

    # 3) 最后兜底：字段没有 choices 限制时，直接返回 prefer 字符串
    return prefer


class WalletServiceTests(TestCase):
    """
    WalletService 单元测试集合

    注意：
    - 使用 TestCase（而不是 TransactionTestCase）：
      这里主要测“业务规则 + 数据写入正确性”，不测并发与真实提交行为。
      并发/行锁类测试建议后续单独用 TransactionTestCase 写在 test_wallet_concurrency.py 中。

    覆盖范围（本文件已实现）：
    - credit 入账：余额变化、流水记录、审计字段
    - debit 扣款：余额变化、流水记录、审计字段
    - debit 余额不足：抛异常且不产生流水（强一致）
    - get_or_create：幂等创建钱包
    """

    def test_credit_should_increase_balance_and_create_transaction(self):
        """
        测试目的：
        - 验证 WalletService.credit 入账逻辑是否正确：
          1) 钱包余额必须 +amount
          2) 必须创建一条 CoinTransaction 流水
          3) 流水审计字段必须准确（change_amount / balance_after / type / ref_type / ref_id）
          4) 如果支持 operator/remark，必须正确落库（可选字段）

        测试步骤：
        1) 准备用户 user（普通用户）
        2) 准备 operator（管理员，用于模拟“后台管理员充值”这种审计场景）
        3) 为 user 准备钱包，初始余额 0
        4) 调用 WalletService.credit 入账 100
        5) 断言：余额=100 + 流水字段正确
        """
        # 1) 前置数据：创建普通用户（代表钱包拥有者）
        user = create_user()

        # 2) 前置数据：创建管理员（代表后台操作人，用于审计字段 operator）
        operator = create_admin()

        # 3) 前置数据：确保钱包存在且初始余额为 0
        #    说明：我们统一用 factory 准备测试初始状态，避免测试里散落 ORM create。
        create_wallet_with_balance(user=user, balance=0)

        # 4) 准备交易类型：优先使用 INIT（如果你的枚举没有 INIT，会自动回退到任意一个合法值）
        tx_type = _pick_tx_type("INIT")

        # 5) 执行业务步骤：调用 Service 入账
        WalletService.credit(
            user=user,
            amount=100,
            tx_type=tx_type,
            ref_type="TEST",   # ref_type/ref_id 用于审计追溯（例如关联订单、会员、活动等）
            ref_id=123,
            operator=operator,  # 后台操作人（可选字段）
            remark="测试入账",   # 审计备注（可选字段）
        )

        # 6) 断言：钱包余额正确
        wallet = Wallet.objects.get(user=user)
        self.assertEqual(wallet.balance, 100)

        # 7) 断言：必须产生一条流水
        #    说明：流水是“审计事实”，余额只是结果；余额正确但无流水 = 不可追溯（严重问题）
        tx = CoinTransaction.objects.filter(user=user).order_by("-id").first()
        self.assertIsNotNone(tx)

        # 8) 断言：核心审计字段正确
        #    change_amount：本次变化金额（入账为正）
        #    balance_after：变化后余额
        self.assertEqual(tx.change_amount, 100)
        self.assertEqual(tx.balance_after, 100)

        #    type/ref_type/ref_id：用于追溯业务来源（必须准确）
        self.assertEqual(tx.type, tx_type)
        self.assertEqual(tx.ref_type, "TEST")
        self.assertEqual(tx.ref_id, 123)

        # 9) 断言：可选审计字段（如果你的模型有这些字段）
        if hasattr(tx, "operator_id"):
            self.assertEqual(tx.operator_id, operator.id)
        if hasattr(tx, "remark"):
            self.assertEqual(tx.remark, "测试入账")

    def test_debit_should_decrease_balance_and_create_transaction(self):
        """
        测试目的：
        - 验证 WalletService.debit 扣款逻辑是否正确：
          1) 钱包余额必须 -amount
          2) 必须创建一条 CoinTransaction 流水
          3) 流水 change_amount 必须为负数
          4) 流水 balance_after 必须为扣款后的余额
          5) ref_type/ref_id/operator/remark 等审计字段必须可追溯

        测试步骤：
        1) 准备用户与管理员
        2) 创建钱包并设置初始余额 200
        3) 调用 debit 扣款 60
        4) 断言：余额=140
        5) 断言：流水 change_amount=-60，balance_after=140，审计字段正确
        """
        # 1) 前置数据：普通用户与管理员
        user = create_user()
        operator = create_admin()

        # 2) 前置数据：钱包初始余额 200
        create_wallet_with_balance(user=user, balance=200)

        # 3) 准备交易类型：优先使用 PURCHASE（不存在则自动回退）
        tx_type = _pick_tx_type("PURCHASE")

        # 4) 执行业务步骤：扣款 60
        WalletService.debit(
            user=user,
            amount=60,
            tx_type=tx_type,
            ref_type="ORDER",  # 这里模拟“订单扣款”
            ref_id=999,
            operator=operator,
            remark="测试扣款",
        )

        # 5) 断言：余额扣减正确（200-60=140）
        wallet = Wallet.objects.get(user=user)
        self.assertEqual(wallet.balance, 140)

        # 6) 断言：必须产生一条扣款流水
        tx = CoinTransaction.objects.filter(user=user).order_by("-id").first()
        self.assertIsNotNone(tx)

        # 7) 断言：扣款流水的关键字段
        #    change_amount：扣款必须为负数
        #    balance_after：扣款后的余额
        self.assertEqual(tx.change_amount, -60)
        self.assertEqual(tx.balance_after, 140)

        #    业务追溯字段
        self.assertEqual(tx.type, tx_type)
        self.assertEqual(tx.ref_type, "ORDER")
        self.assertEqual(tx.ref_id, 999)

        # 8) 断言：可选字段
        if hasattr(tx, "operator_id"):
            self.assertEqual(tx.operator_id, operator.id)
        if hasattr(tx, "remark"):
            self.assertEqual(tx.remark, "测试扣款")

    def test_debit_should_raise_when_balance_not_enough_and_no_transaction_created(self):
        """
        测试目的：
        - 验证“余额不足”场景必须符合强一致原则：
          1) debit 必须抛 BalanceNotEnough
          2) 钱包余额不能发生任何变化
          3) 不能产生任何新的 CoinTransaction 流水
             （失败不应留下“扣款流水”，否则审计会误导）

        测试步骤：
        1) 创建用户并设置钱包余额为 10
        2) 记录扣款前的钱包余额与流水数量
        3) 调用 debit 扣 11（必然余额不足）
        4) 断言抛 BalanceNotEnough
        5) 再次读取钱包余额与流水数量
        6) 断言：余额不变、流水数量不变
        """
        # 1) 前置数据：创建用户并设置初始余额 10
        user = create_user()
        create_wallet_with_balance(user=user, balance=10)

        # 2) 记录扣款前状态：余额、流水数量
        tx_type = _pick_tx_type("PURCHASE")
        before_wallet = Wallet.objects.get(user=user)
        before_tx_count = CoinTransaction.objects.filter(user=user).count()

        # 3) 执行业务步骤：扣款 11 -> 预期必须抛异常
        with self.assertRaises(BalanceNotEnough):
            WalletService.debit(
                user=user,
                amount=11,
                tx_type=tx_type,
                ref_type="ORDER",
                ref_id=1,
                remark="余额不足应失败",
            )

        # 4) 断言失败后的状态：余额不变、流水不新增
        after_wallet = Wallet.objects.get(user=user)
        after_tx_count = CoinTransaction.objects.filter(user=user).count()

        self.assertEqual(after_wallet.balance, before_wallet.balance)
        self.assertEqual(after_tx_count, before_tx_count)

    def test_get_or_create_should_create_wallet_when_missing(self):
        """
        测试目的：
        - 验证 WalletService.get_or_create 的幂等性与自动创建能力：
          1) 用户没有钱包记录时，调用 get_or_create 必须创建钱包
          2) 多次调用 get_or_create 必须返回同一个钱包（幂等）

        测试步骤：
        1) 创建用户（此时数据库中应不存在 wallet）
        2) 断言 wallet 不存在（前置校验，避免脏数据影响测试）
        3) 调用 WalletService.get_or_create -> 应创建并返回 wallet
        4) 断言 wallet 存在且有 id
        5) 再调用一次 -> 返回同一条记录（id 相同）
        """
        # 1) 前置数据：创建用户
        user = create_user()

        # 2) 前置校验：确保该用户没有钱包（避免测试被历史数据污染）
        self.assertFalse(Wallet.objects.filter(user=user).exists())

        # 3) 执行业务步骤：首次调用应创建钱包
        wallet = WalletService.get_or_create(user)
        self.assertIsNotNone(wallet)
        self.assertIsNotNone(wallet.id)
        self.assertTrue(Wallet.objects.filter(user=user).exists())

        # 4) 幂等性校验：第二次调用仍应返回同一个钱包
        wallet2 = WalletService.get_or_create(user)
        self.assertEqual(wallet.id, wallet2.id)
