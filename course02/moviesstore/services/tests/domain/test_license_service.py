from __future__ import annotations

"""
本测试文件用于验证：LicenseService（授权领域服务）的核心业务行为是否正确？

覆盖范围（与 docs/10 Service层单元测试.md 对齐）：
1. grant_purchase_license 创建成功
2. 重复授权 -> BusinessRuleViolation 且不产生重复数据
3. has_movie_access 权限判断（购买/会员/无权限）

同时补充：
- grant_license_force 强制授权的兜底逻辑
- get_license / has_purchase_license / list_licenses / list_user_licenses 的查询行为
"""

from django.test import TestCase

from apps.orders.models import PurchaseLicense, PurchaseOrder, PurchaseOrderItem
from services.common.exceptions import BusinessRuleViolation, NotFound
from services.domain.license_service import LicenseService
from services.tests.factories.movie_factory import create_movie
from services.tests.factories.membership_factory import (
    create_active_membership,
    create_expired_membership,
)
from services.tests.factories.order_factory import create_order
from services.tests.factories.user_factory import create_user


def _create_order_item(*, user, movie) -> PurchaseOrderItem:
    """
    测试辅助：为用户创建单电影订单，并返回对应的订单项
    """
    order = create_order(user=user, movies=[movie])
    item = PurchaseOrderItem.objects.filter(order=order).first()
    if not item:
        raise AssertionError("测试订单项创建失败")
    return item


class LicenseServiceTests(TestCase):
    """
    LicenseService 单元测试集合
    """

    def test_grant_purchase_license_should_create_license(self):
        """
        测试目的：
        - grant_purchase_license 能正确创建授权记录
        - 授权记录字段应与 user/movie/order_item 一致

        测试步骤：
        1. 准备测试数据：创建用户、电影和对应订单项
        2. 调用 grant_purchase_license 方法创建授权
        3. 验证授权记录是否成功创建
        4. 验证授权记录字段是否正确关联
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()
        order_item = _create_order_item(user=user, movie=movie)

        # 2. 执行授权创建操作
        license_obj = LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=order_item,
        )

        # 3. 验证授权记录是否成功创建
        self.assertIsNotNone(license_obj.id)
        
        # 4. 验证授权记录字段是否正确关联
        self.assertEqual(license_obj.user_id, user.id)
        self.assertEqual(license_obj.movie_id, movie.id)
        self.assertEqual(license_obj.order_item_id, order_item.id)

    def test_grant_purchase_license_should_raise_when_order_item_missing(self):
        """
        测试目的：
        - order_item 为空时必须抛 BusinessRuleViolation
        - 不允许产生脏数据

        测试步骤：
        1. 准备测试数据：创建用户和电影
        2. 调用 grant_purchase_license 方法，传入 None 作为 order_item
        3. 验证是否抛出 BusinessRuleViolation 异常
        4. 验证是否未创建授权记录（无脏数据）
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()

        # 2. 调用方法并验证异常
        with self.assertRaises(BusinessRuleViolation):
            LicenseService.grant_purchase_license(
                user=user,
                movie=movie,
                order_item=None,
            )

        # 3. 验证无脏数据产生
        self.assertFalse(PurchaseLicense.objects.filter(user=user, movie=movie).exists())

    def test_grant_purchase_license_should_raise_on_duplicate(self):
        """
        测试目的：
        - 同一用户对同一电影不能重复授权
        - 再次授予应抛 BusinessRuleViolation
        - 授权记录数量不应增加

        测试步骤：
        1. 准备测试数据：创建用户和电影
        2. 首次授权：创建订单项并授予授权
        3. 验证首次授权成功
        4. 再次授权：为同一用户和电影创建新订单项并尝试再次授予授权
        5. 验证是否抛出 BusinessRuleViolation 异常
        6. 验证授权记录数量仍为1（无重复数据）
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()

        # 2. 首次授权
        first_item = _create_order_item(user=user, movie=movie)
        first_license = LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=first_item,
        )
        
        # 3. 验证首次授权成功
        self.assertIsNotNone(first_license.id)

        # 4. 尝试重复授权
        second_item = _create_order_item(user=user, movie=movie)
        with self.assertRaises(BusinessRuleViolation):
            LicenseService.grant_purchase_license(
                user=user,
                movie=movie,
                order_item=second_item,
            )

        # 5. 验证授权记录数量未增加
        self.assertEqual(
            PurchaseLicense.objects.filter(user=user, movie=movie).count(),
            1,
        )

    def test_grant_license_force_should_create_virtual_order_when_missing(self):
        """
        测试目的：
        - grant_license_force 在无授权时应创建授权记录
        - 必须挂载一个“虚拟订单项”，并具备基础审计字段（0 金币、完成状态）

        测试步骤：
        1. 准备测试数据：创建用户和电影
        2. 调用 grant_license_force 方法强制授予授权
        3. 验证授权记录是否成功创建
        4. 验证是否创建了虚拟订单项和订单
        5. 验证虚拟订单的属性是否正确（0金币、完成状态）
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()

        # 2. 执行强制授权操作
        license_obj = LicenseService.grant_license_force(
            user=user,
            movie=movie,
            operator=None,
            remark="测试强制授权",
        )

        # 3. 验证授权记录成功创建
        self.assertIsNotNone(license_obj.id)
        
        # 4. 获取并验证虚拟订单项和订单
        order_item = PurchaseOrderItem.objects.get(id=license_obj.order_item_id)
        order = PurchaseOrder.objects.get(id=order_item.order_id)

        # 5. 验证虚拟订单属性
        self.assertEqual(order.total_coin, 0)  # 虚拟订单金额为0
        self.assertEqual(order.status, PurchaseOrder.Status.COMPLETED)  # 状态为已完成
        self.assertEqual(order_item.price_coin, 0)  # 订单项价格为0
        self.assertEqual(order_item.movie_id, movie.id)  # 订单项关联正确电影

    def test_grant_license_force_should_return_existing_license(self):
        """
        测试目的：
        - 已存在授权时，grant_license_force 应返回同一条记录
        - 不应额外创建重复授权

        测试步骤：
        1. 准备测试数据：创建用户和电影
        2. 创建订单项并授予正常授权
        3. 记录授权记录数量
        4. 调用 grant_license_force 方法尝试强制授权
        5. 验证返回的授权记录与原记录相同
        6. 验证授权记录数量未增加
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()
        
        # 2. 创建正常授权
        item = _create_order_item(user=user, movie=movie)
        lic = LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=item,
        )

        # 3. 记录授权记录数量
        before_count = PurchaseLicense.objects.filter(user=user, movie=movie).count()
        
        # 4. 尝试强制授权
        lic2 = LicenseService.grant_license_force(user=user, movie=movie)
        
        # 5. 记录授权记录数量
        after_count = PurchaseLicense.objects.filter(user=user, movie=movie).count()

        # 6. 验证返回的是同一条记录
        self.assertEqual(lic.id, lic2.id)
        
        # 7. 验证未创建重复授权
        self.assertEqual(before_count, after_count)

    def test_get_license_should_return_or_raise_not_found(self):
        """
        测试目的：
        - get_license 在无授权时抛 NotFound
        - 有授权时返回正确记录

        测试步骤：
        1. 准备测试数据：创建用户和电影
        2. 调用 get_license 方法尝试获取不存在的授权
        3. 验证是否抛出 NotFound 异常
        4. 创建订单项并授予授权
        5. 再次调用 get_license 方法获取授权
        6. 验证返回的授权记录与创建的记录相同
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()

        # 2. 尝试获取不存在的授权
        with self.assertRaises(NotFound):
            LicenseService.get_license(user=user, movie=movie)

        # 3. 创建授权
        item = _create_order_item(user=user, movie=movie)
        lic = LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=item,
        )
        
        # 4. 获取授权并验证
        got = LicenseService.get_license(user=user, movie=movie)
        self.assertEqual(got.id, lic.id)

    def test_has_purchase_license_should_reflect_state(self):
        """
        测试目的：
        - has_purchase_license 应正确返回是否存在购买授权

        测试步骤：
        1. 准备测试数据：创建用户和电影
        2. 调用 has_purchase_license 方法检查未授权状态
        3. 验证返回 False（无授权）
        4. 创建订单项并授予授权
        5. 再次调用 has_purchase_license 方法检查授权状态
        6. 验证返回 True（有授权）
        """
        # 1. 准备测试数据
        user = create_user()
        movie = create_movie()

        # 2. 检查未授权状态
        self.assertFalse(LicenseService.has_purchase_license(user=user, movie=movie))

        # 3. 创建授权
        item = _create_order_item(user=user, movie=movie)
        LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=item,
        )
        
        # 4. 检查授权状态
        self.assertTrue(LicenseService.has_purchase_license(user=user, movie=movie))

    def test_list_licenses_should_filter(self):
        """
        测试目的：
        - list_licenses 支持 user/movie/order_id 过滤

        测试步骤：
        1. 准备测试数据：创建2个用户和2个电影
        2. 为用户1创建电影1和电影2的授权
        3. 为用户2创建电影1的授权
        4. 测试按用户过滤：验证用户1有2个授权
        5. 测试按电影过滤：验证电影1有2个授权
        6. 测试按订单ID过滤：验证只返回对应订单的授权
        7. 测试无过滤：验证返回所有授权
        """
        # 1. 准备测试数据
        user1 = create_user()
        user2 = create_user()
        movie1 = create_movie()
        movie2 = create_movie()

        # 2. 创建授权数据
        # 用户1 - 电影1 授权
        item_11 = _create_order_item(user=user1, movie=movie1)
        lic_11 = LicenseService.grant_purchase_license(
            user=user1,
            movie=movie1,
            order_item=item_11,
        )
        # 用户1 - 电影2 授权
        item_12 = _create_order_item(user=user1, movie=movie2)
        lic_12 = LicenseService.grant_purchase_license(
            user=user1,
            movie=movie2,
            order_item=item_12,
        )
        # 用户2 - 电影1 授权
        item_21 = _create_order_item(user=user2, movie=movie1)
        lic_21 = LicenseService.grant_purchase_license(
            user=user2,
            movie=movie1,
            order_item=item_21,
        )

        # 3. 测试按用户过滤
        self.assertEqual(LicenseService.list_licenses(user=user1).count(), 2)  # 用户1有2个授权
        
        # 4. 测试按电影过滤
        self.assertEqual(LicenseService.list_licenses(movie=movie1).count(), 2)  # 电影1有2个授权

        # 5. 测试按订单ID过滤
        order_id = PurchaseOrderItem.objects.get(id=lic_12.order_item_id).order_id
        qs = LicenseService.list_licenses(order_id=order_id)
        self.assertEqual(qs.count(), 1)  # 订单对应1个授权
        self.assertEqual(qs.first().id, lic_12.id)  # 授权ID匹配

        # 6. 测试无过滤
        all_ids = {lic_11.id, lic_12.id, lic_21.id}
        self.assertEqual(
            set(LicenseService.list_licenses().values_list("id", flat=True)),
            all_ids,  # 返回所有授权
        )

    def test_list_user_licenses_should_only_return_user_records(self):
        """
        测试目的：
        - list_user_licenses 只返回指定用户的授权记录

        测试步骤：
        1. 准备测试数据：创建2个用户和2个电影
        2. 为用户1创建电影1和电影2的授权
        3. 为用户2创建电影1的授权
        4. 调用 list_user_licenses 获取用户1的授权列表
        5. 验证返回的授权数量为2
        6. 验证返回的所有授权都属于用户1
        """
        # 1. 准备测试数据
        user1 = create_user()
        user2 = create_user()
        movie1 = create_movie()
        movie2 = create_movie()

        # 2. 创建授权数据
        # 用户1 - 电影1 授权
        LicenseService.grant_purchase_license(
            user=user1,
            movie=movie1,
            order_item=_create_order_item(user=user1, movie=movie1),
        )
        # 用户1 - 电影2 授权
        LicenseService.grant_purchase_license(
            user=user1,
            movie=movie2,
            order_item=_create_order_item(user=user1, movie=movie2),
        )
        # 用户2 - 电影1 授权
        LicenseService.grant_purchase_license(
            user=user2,
            movie=movie1,
            order_item=_create_order_item(user=user2, movie=movie1),
        )

        # 3. 获取用户1的授权列表
        qs = LicenseService.list_user_licenses(user=user1)
        
        # 4. 验证授权数量
        self.assertEqual(qs.count(), 2)  # 用户1应有2个授权
        
        # 5. 验证所有授权都属于用户1
        self.assertTrue(all(item.user_id == user1.id for item in qs))

    def test_has_movie_access_should_consider_purchase_and_membership(self):
        """
        测试目的：
        - 有购买授权 -> True
        - 无购买授权但会员有效 -> True
        - 都没有 -> False
        - include_membership=False 时不应放行会员权限

        测试步骤：
        1. 准备测试数据：创建电影
        2. 创建3个用户：有购买授权的用户、有有效会员的用户、无访问权限的用户
        3. 为有购买授权的用户创建电影授权
        4. 为有有效会员的用户创建活跃会员
        5. 为无访问权限的用户创建过期会员
        6. 测试有购买授权的用户：验证返回True
        7. 测试有有效会员的用户：验证返回True
        8. 测试无访问权限的用户：验证返回False
        9. 测试有有效会员但禁用会员权限的情况：验证返回False
        """
        # 1. 准备测试数据
        movie = create_movie()

        # 2. 创建测试用户
        user_with_license = create_user()  # 有购买授权的用户
        user_with_membership = create_user()  # 有有效会员的用户
        user_without_access = create_user()  # 无访问权限的用户

        # 3. 设置用户权限
        # 为用户1创建电影购买授权
        LicenseService.grant_purchase_license(
            user=user_with_license,
            movie=movie,
            order_item=_create_order_item(user=user_with_license, movie=movie),
        )
        # 为用户2创建活跃会员
        create_active_membership(user=user_with_membership)
        # 为用户3创建过期会员（无权限）
        create_expired_membership(user=user_without_access)

        # 4. 测试有购买授权的用户
        self.assertTrue(
            LicenseService.has_movie_access(user=user_with_license, movie=movie)
        )
        
        # 5. 测试有有效会员的用户
        self.assertTrue(
            LicenseService.has_movie_access(user=user_with_membership, movie=movie)
        )
        
        # 6. 测试无访问权限的用户
        self.assertFalse(
            LicenseService.has_movie_access(user=user_without_access, movie=movie)
        )
        
        # 7. 测试禁用会员权限的情况
        self.assertFalse(
            LicenseService.has_movie_access(
                user=user_with_membership,
                movie=movie,
                include_membership=False,
            )
        )
