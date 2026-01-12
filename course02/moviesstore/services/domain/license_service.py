# services/domain/license_service.py
from django.db import transaction, IntegrityError

from apps.orders.models import PurchaseLicense, PurchaseOrderItem
from services.common.exceptions import NotFound, BusinessRuleViolation
from services.domain.membership_service import MembershipService


class LicenseService:
    """
    授权域 Service（CRUD + 权限判断）

    职责边界：
    - 负责“购买授权（PurchaseLicense）”的创建与查询
    - 提供统一的权限判断接口（支持：购买授权 + 会员权限）
    - 为后台管理系统与 App/Web 端提供统一能力

    说明：
    - 会员不是 PurchaseLicense 记录，本质是“时间段权限”
    - 权限判断时：购买授权 OR 会员有效 -> 允许访问
    """

    # =============================
    # 写：授权发放（购买）
    # =============================

    @staticmethod
    @transaction.atomic
    def grant_purchase_license(*, user, movie, order_item: PurchaseOrderItem) -> PurchaseLicense:
        """
        发放购买授权（强一致）
        - 一个用户对同一电影只能有一条购买授权
        - 必须传入 order_item 用于审计追溯

        并发安全：
        - 数据库 unique_together(user, movie) 做最终防线
        - 捕获 IntegrityError 转为业务异常
        """
        if not order_item:
            raise BusinessRuleViolation("order_item 不能为空")

        # 业务层先查一遍，给更友好的错误（并发下仍可能被 unique 兜底）
        if PurchaseLicense.objects.filter(user=user, movie=movie).exists():
            raise BusinessRuleViolation("用户已拥有该电影授权")

        try:
            return PurchaseLicense.objects.create(
                user=user,
                movie=movie,
                order_item=order_item,
            )
        except IntegrityError:
            # 并发情况下两次 create 竞争 unique_together
            raise BusinessRuleViolation("用户已拥有该电影授权")

    @staticmethod
    @transaction.atomic
    def grant_license_force(*, user, movie, operator=None, remark: str | None = None) -> PurchaseLicense:
        """
        强制发放授权（后台运营/补偿场景）
        注意：
        - PurchaseLicense 需要 order_item（模型约束），强制授权时通常没有真实订单
        - 推荐做法：为“强制授权”设计独立模型/字段或生成一条“运营订单”
        - 为保持与你现有模型兼容，这里采用“创建一条虚拟订单项”的方式（最小可用）

        如果你不希望创建虚拟订单，则应修改 PurchaseLicense 模型让 order_item 可空。
        """
        from apps.orders.models import PurchaseOrder, PurchaseOrderItem  # 避免循环 import
        from django.utils import timezone

        if PurchaseLicense.objects.filter(user=user, movie=movie).exists():
            return PurchaseLicense.objects.get(user=user, movie=movie)

        # 创建一条“运营订单”（0 金币），用于挂载 order_item，便于审计
        order = PurchaseOrder.objects.create(
            user=user,
            total_coin=0,
            status=PurchaseOrder.Status.COMPLETED,
            created_at=timezone.now(),
        )
        item = PurchaseOrderItem.objects.create(
            order=order,
            movie=movie,
            price_coin=0,
        )

        try:
            return PurchaseLicense.objects.create(
                user=user,
                movie=movie,
                order_item=item,
            )
        except IntegrityError:
            return PurchaseLicense.objects.get(user=user, movie=movie)

    # =============================
    # 读：授权查询（CRUD）
    # =============================

    @staticmethod
    def get_license(*, user, movie) -> PurchaseLicense:
        """
        获取用户对某电影的购买授权
        """
        lic = PurchaseLicense.objects.select_related("user", "movie", "order_item").filter(
            user=user,
            movie=movie,
        ).first()
        if not lic:
            raise NotFound("购买授权不存在")
        return lic

    @staticmethod
    def has_purchase_license(*, user, movie) -> bool:
        """
        是否存在购买授权（只看 PurchaseLicense，不看会员）
        """
        return PurchaseLicense.objects.filter(user=user, movie=movie).exists()

    @staticmethod
    def list_licenses(
        *,
        user=None,
        movie=None,
        order_id=None,
    ):
        """
        后台/运营授权查询列表（QuerySet 返回，调用方自行分页）

        支持筛选：
        - user
        - movie
        - order_id（通过 order_item -> order_id 反查）
        """
        qs = PurchaseLicense.objects.select_related("user", "movie", "order_item", "order_item__order").all()

        if user is not None:
            qs = qs.filter(user=user)

        if movie is not None:
            qs = qs.filter(movie=movie)

        if order_id is not None:
            qs = qs.filter(order_item__order_id=order_id)

        return qs.order_by("-created_at")

    @staticmethod
    def list_user_licenses(*, user):
        """
        用户中心：我的购买电影列表（只看购买授权）
        """
        return (
            PurchaseLicense.objects.select_related("movie")
            .filter(user=user)
            .order_by("-created_at")
        )

    # =============================
    # 权限判断：购买授权 + 会员
    # =============================

    @staticmethod
    def has_movie_access(*, user, movie, include_membership: bool = True) -> bool:
        """
        统一的“是否可观看/下载”权限判断

        规则：
        - 有购买授权 -> True
        - 否则（可选）会员有效 -> True
        - 否则 -> False

        参数：
        - include_membership：是否把会员视为可访问来源（默认 True）
        """
        if PurchaseLicense.objects.filter(user=user, movie=movie).exists():
            return True

        if include_membership and MembershipService.is_active(user):
            return True

        return False
