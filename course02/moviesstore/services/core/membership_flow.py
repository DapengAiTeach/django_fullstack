from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.membership.models import Membership
from apps.wallet.models import CoinTransaction
from services.common.exceptions import BusinessRuleViolation, NotFound
from services.domain.wallet_service import WalletService


class MembershipFlow:
    """
    会员闭环（强一致事务）
    目标：
    - 通过钱包扣减金币（或未来接入支付后的入账）
    - 开通/续费会员
    - 记录资金流水（由 WalletService 统一写入）
    - 形成可审计、可回滚的闭环
    """

    # 会员套餐的“默认时长”配置（可根据你的产品策略调整）
    # 说明：
    # - MONTH：30 天
    # - YEAR：365 天
    PLAN_DURATION_DAYS = {
        Membership.Plan.MONTH: 30,
        Membership.Plan.YEAR: 365,
    }

    @staticmethod
    @transaction.atomic
    def open_or_renew_by_coin(
        *,
        user,
        plan: str,
        price_coin: int,
        operator=None,
        remark: str | None = None,
    ) -> Membership:
        """
        使用金币开通/续费会员（闭环）

        参数：
        - user: 会员用户
        - plan: Membership.Plan.MONTH / Membership.Plan.YEAR
        - price_coin: 本次开通/续费扣减金币数量（由上层传入，便于支持运营活动/折扣）
        - operator: 管理员操作时可传入（审计）
        - remark: 备注信息（可用于记录活动、来源等）

        返回：
        - Membership 记录（最新状态）
        """

        if price_coin <= 0:
            raise BusinessRuleViolation("会员价格必须大于 0")

        if plan not in (Membership.Plan.MONTH, Membership.Plan.YEAR):
            raise BusinessRuleViolation("非法会员套餐类型")

        duration_days = MembershipFlow.PLAN_DURATION_DAYS.get(plan)
        if not duration_days:
            raise BusinessRuleViolation("未配置该会员套餐的时长")

        # 1) 先扣金币（行级锁 + 不允许负数，由 WalletService 保证）
        # ref_type/ref_id 用于审计追溯：这里用 membership 作为业务类型
        # ref_id 需要在创建/更新会员记录后才能确定，因此这里先创建会员记录占位或先扣款后再写入 ref_id
        # 为保证审计一致性：本实现采用“先创建/续费会员记录，再扣款写流水”，整体事务保证回滚一致。
        now = timezone.now()

        # 2) 获取当前会员记录（如果存在）
        current = (
            Membership.objects.select_for_update()
            .filter(user=user)
            .order_by("-end_at")
            .first()
        )

        # 3) 计算新的 start_at / end_at
        # 规则：
        # - 当前会员仍在有效期内（end_at >= now）：从当前 end_at 继续往后续
        # - 当前会员已过期：从 now 开始
        if current and current.end_at and current.end_at >= now:
            start_at = current.start_at  # 保留原 start_at（也可以选择不变）
            end_base = current.end_at
        else:
            start_at = now
            end_base = now

        new_end_at = end_base + timedelta(days=duration_days)

        # 4) 写入/更新会员记录
        # 这里策略采用“每个用户保留一条会员记录”，续费则更新 end_at（推荐）
        if current and Membership.objects.filter(id=current.id).exists():
            current.plan = plan
            current.status = Membership.Status.ACTIVE
            # 如果之前过期，从 now 开始重置 start_at
            current.start_at = start_at
            current.end_at = new_end_at
            current.save(update_fields=["plan", "status", "start_at", "end_at"])
            membership = current
        else:
            membership = Membership.objects.create(
                user=user,
                plan=plan,
                status=Membership.Status.ACTIVE,
                start_at=start_at,
                end_at=new_end_at,
            )

        # 5) 扣减金币并写流水（强制使用 WalletService 统一入口）
        WalletService.debit(
            user=user,
            amount=price_coin,
            tx_type=CoinTransaction.TxType.RENEW,
            ref_type="MEMBERSHIP",
            ref_id=membership.id,
            operator=operator,
            remark=remark or f"开通/续费会员：{plan}",
        )

        return membership

    @staticmethod
    def get_active_membership(user) -> Membership | None:
        """
        获取用户当前有效会员（读操作，不加锁）
        """
        now = timezone.now()
        return (
            Membership.objects.filter(
                user=user,
                status=Membership.Status.ACTIVE,
                start_at__lte=now,
                end_at__gte=now,
            )
            .order_by("-end_at")
            .first()
        )

    @staticmethod
    def is_active(user) -> bool:
        """
        判断用户当前是否为有效会员（读操作）
        """
        return MembershipFlow.get_active_membership(user) is not None
