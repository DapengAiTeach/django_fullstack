# services/domain/membership_service.py
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.membership.models import Membership
from services.common.exceptions import NotFound, BusinessRuleViolation


class MembershipService:
    """
    会员域 Service（CRUD + 状态管理 + 权限判断）

    职责边界：
    - 负责 Membership 记录的创建/更新/查询/状态刷新
    - 不处理扣费/支付/金币流水（这些属于 core/membership_flow.py 的闭环职责）
    - 为后台管理系统与 App/Web 端提供统一的“会员状态/有效期”能力

    关键原则：
    - 会员有效性以 (status=ACTIVE 且 now 在 start_at~end_at 范围内) 为准
    - 续费规则：未过期则从 end_at 续；已过期则从 now 开始
    """

    # 会员套餐默认时长配置（可按产品改为“自然月/自然年”等更复杂规则）
    PLAN_DURATION_DAYS = {
        Membership.Plan.MONTH: 30,
        Membership.Plan.YEAR: 365,
    }

    # =============================
    # 基础读：查询与判断
    # =============================

    @staticmethod
    def get_latest(user):
        """
        获取用户最新一条会员记录（按 end_at 倒序）
        """
        return (
            Membership.objects.filter(user=user)
            .order_by("-end_at")
            .first()
        )

    @staticmethod
    def get_active(user):
        """
        获取用户当前有效会员（只读）
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
        判断用户是否为有效会员（只读）
        """
        return MembershipService.get_active(user) is not None

    @staticmethod
    def get_status(user) -> dict:
        """
        获取用户会员状态摘要（给 App/Web 端和后台都能直接用）
        """
        m = MembershipService.get_latest(user)
        if not m:
            return {
                "has_membership": False,
                "is_active": False,
                "plan": None,
                "status": None,
                "start_at": None,
                "end_at": None,
            }

        now = timezone.now()
        active = (
            m.status == Membership.Status.ACTIVE
            and m.start_at <= now <= m.end_at
        )
        return {
            "has_membership": True,
            "is_active": active,
            "plan": m.plan,
            "status": m.status,
            "start_at": m.start_at,
            "end_at": m.end_at,
        }

    # =============================
    # 写：开通/续费（不含扣费）
    # =============================

    @staticmethod
    @transaction.atomic
    def open_or_renew(
        *,
        user,
        plan: str,
        duration_days: int = None,
        start_from_now_if_expired: bool = True,
    ) -> Membership:
        """
        开通/续费会员（只负责 Membership 记录，不含扣费）

        参数：
        - plan: Membership.Plan.MONTH / Membership.Plan.YEAR
        - duration_days: 可传入自定义天数（活动/补偿），不传则按套餐默认
        - start_from_now_if_expired:
            - True：已过期则从 now 重新开始
            - False：已过期仍从原 end_at 继续（一般不这么做）

        规则：
        - 当前有效：从当前 end_at 往后续
        - 当前过期：从 now 开始（默认）
        """
        if plan not in (Membership.Plan.MONTH, Membership.Plan.YEAR):
            raise BusinessRuleViolation("非法会员套餐类型")

        if duration_days is None:
            duration_days = MembershipService.PLAN_DURATION_DAYS.get(plan)

        if not duration_days or duration_days <= 0:
            raise BusinessRuleViolation("会员时长必须大于 0")

        now = timezone.now()

        # 对该用户会员记录加锁，避免并发续费导致 end_at 错乱
        current = (
            Membership.objects.select_for_update()
            .filter(user=user)
            .order_by("-end_at")
            .first()
        )

        if current and current.end_at and current.end_at >= now:
            # 仍有效：从 end_at 续
            start_at = current.start_at
            end_base = current.end_at
        else:
            # 已过期/不存在：从 now 开始（推荐策略）
            if start_from_now_if_expired:
                start_at = now
                end_base = now
            else:
                # 少数场景：从旧 end_at 继续（不推荐）
                start_at = current.start_at if current else now
                end_base = current.end_at if current and current.end_at else now

        new_end_at = end_base + timedelta(days=duration_days)

        if current:
            current.plan = plan
            current.status = Membership.Status.ACTIVE
            current.start_at = start_at
            current.end_at = new_end_at
            current.save(update_fields=["plan", "status", "start_at", "end_at"])
            return current

        return Membership.objects.create(
            user=user,
            plan=plan,
            status=Membership.Status.ACTIVE,
            start_at=start_at,
            end_at=new_end_at,
        )

    # =============================
    # 写：状态刷新/过期处理（不含定时任务，仅提供能力）
    # =============================

    @staticmethod
    @transaction.atomic
    def refresh_status(user) -> Membership:
        """
        刷新某用户会员状态：
        - 如果 end_at < now 且 status 仍为 ACTIVE，则置为 EXPIRED
        - 返回最新会员记录（若不存在则抛 NotFound）
        """
        m = (
            Membership.objects.select_for_update()
            .filter(user=user)
            .order_by("-end_at")
            .first()
        )
        if not m:
            raise NotFound("会员记录不存在")

        now = timezone.now()
        if m.status == Membership.Status.ACTIVE and m.end_at < now:
            m.status = Membership.Status.EXPIRED
            m.save(update_fields=["status"])

        return m

    @staticmethod
    @transaction.atomic
    def set_status(*, membership_id: int, status: str) -> Membership:
        """
        后台管理能力：强制设置会员状态（运营/风控/补偿场景）
        注意：这是“管理行为”，调用方需自行做权限控制与审计记录
        """
        if status not in (Membership.Status.ACTIVE, Membership.Status.GRACE, Membership.Status.EXPIRED):
            raise BusinessRuleViolation("非法会员状态")

        m = Membership.objects.select_for_update().filter(id=membership_id).first()
        if not m:
            raise NotFound("会员记录不存在")

        m.status = status
        m.save(update_fields=["status"])
        return m

    @staticmethod
    @transaction.atomic
    def extend_end_at(*, membership_id: int, extra_days: int) -> Membership:
        """
        后台管理能力：延长会员有效期（补偿/活动）
        - extra_days 必须 > 0
        - 若已过期，默认从 now 开始延长（避免 end_at 停留在过去）
        """
        if extra_days <= 0:
            raise BusinessRuleViolation("延长天数必须大于 0")

        now = timezone.now()
        m = Membership.objects.select_for_update().filter(id=membership_id).first()
        if not m:
            raise NotFound("会员记录不存在")

        # 若 end_at 在过去，则从 now 作为基准
        base = m.end_at if m.end_at and m.end_at >= now else now
        m.end_at = base + timedelta(days=extra_days)

        # 延长后通常应视为生效中（业务可按需调整）
        if m.end_at >= now:
            m.status = Membership.Status.ACTIVE
            if m.start_at > now:
                m.start_at = now

        m.save(update_fields=["start_at", "end_at", "status"])
        return m

    # =============================
    # 后台查询（CRUD）
    # =============================

    @staticmethod
    def list_memberships(*, user=None, status=None, plan=None):
        """
        后台列表查询（返回 QuerySet，调用方自行分页）
        """
        qs = Membership.objects.all().select_related("user")

        if user is not None:
            qs = qs.filter(user=user)

        if status:
            qs = qs.filter(status=status)

        if plan:
            qs = qs.filter(plan=plan)

        return qs.order_by("-end_at")
