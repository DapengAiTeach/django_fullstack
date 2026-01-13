# 10 Service层单元测试



## 目录结构

```bash
services/
├── common/
│   ├── __init__.py
│   ├── base.py
│   └── exceptions.py
│
├── domain/
│   ├── __init__.py
│   ├── movie_service.py
│   ├── identity_service.py
│   ├── user_service.py
│   ├── wallet_service.py
│   ├── order_service.py
│   ├── license_service.py
│   ├── membership_service.py
│   └── download_service.py
│
├── core/
│   ├── __init__.py
│   ├── purchase_flow.py
│   ├── membership_flow.py
│   └── download_flow.py
│
└── tests/
    ├── __init__.py
    │
    ├── factories/
    │   ├── __init__.py
    │   ├── user_factory.py
    │   ├── movie_factory.py
    │   ├── wallet_factory.py
    │   ├── order_factory.py
    │   ├── license_factory.py
    │   ├── membership_factory.py
    │   └── download_factory.py
    │
    ├── domain/
    │   ├── __init__.py
    │   ├── test_movie_service.py
    │   ├── test_identity_service.py
    │   ├── test_user_service.py
    │   ├── test_wallet_service.py
    │   ├── test_order_service.py
    │   ├── test_license_service.py
    │   ├── test_membership_service.py
    │   └── test_download_service.py
    │
    ├── core/
    │   ├── __init__.py
    │   ├── test_purchase_flow.py
    │   ├── test_membership_flow.py
    │   └── test_download_flow.py
    │
    └── integration/
        ├── __init__.py
        ├── test_purchase_full_chain.py
        └── test_membership_full_chain.py
```



## 展开目录

### Service 业务代码目录

```
services/__init__.py

services/common/__init__.py
services/common/base.py
services/common/exceptions.py

services/domain/__init__.py
services/domain/movie_service.py
services/domain/identity_service.py
services/domain/user_service.py
services/domain/wallet_service.py
services/domain/order_service.py
services/domain/license_service.py
services/domain/membership_service.py
services/domain/download_service.py

services/core/__init__.py
services/core/purchase_flow.py
services/core/membership_flow.py
services/core/download_flow.py
```



### Service 单元测试

```
services/tests/__init__.py
```



### 测试工厂

```
services/tests/factories/__init__.py

services/tests/factories/user_factory.py
services/tests/factories/movie_factory.py
services/tests/factories/wallet_factory.py
services/tests/factories/order_factory.py
services/tests/factories/license_factory.py
services/tests/factories/membership_factory.py
services/tests/factories/download_factory.py
```



### Domain Service 单元测试

```
services/tests/domain/__init__.py

services/tests/domain/test_movie_service.py
services/tests/domain/test_identity_service.py
services/tests/domain/test_user_service.py
services/tests/domain/test_wallet_service.py
services/tests/domain/test_order_service.py
services/tests/domain/test_license_service.py
services/tests/domain/test_membership_service.py
services/tests/domain/test_download_service.py
```



### Core Flow 单元测试

```
services/tests/core/__init__.py

services/tests/core/test_purchase_flow.py
services/tests/core/test_membership_flow.py
services/tests/core/test_download_flow.py
```



### 集成测试

> 这部分文件**数量少，但价值最高**

```
services/tests/integration/__init__.py

services/tests/integration/test_purchase_full_chain.py
services/tests/integration/test_membership_full_chain.py
```



## 创建目录结构

### 创建 services 业务代码目录

```powershell
# services 根目录
New-Item -ItemType Directory -Path "services" -Force

# common
New-Item -ItemType Directory -Path "services\common" -Force
New-Item -ItemType File -Path "services\common\__init__.py" -Force
New-Item -ItemType File -Path "services\common\base.py" -Force
New-Item -ItemType File -Path "services\common\exceptions.py" -Force

# domain
New-Item -ItemType Directory -Path "services\domain" -Force
New-Item -ItemType File -Path "services\domain\__init__.py" -Force
New-Item -ItemType File -Path "services\domain\movie_service.py" -Force
New-Item -ItemType File -Path "services\domain\identity_service.py" -Force
New-Item -ItemType File -Path "services\domain\user_service.py" -Force
New-Item -ItemType File -Path "services\domain\wallet_service.py" -Force
New-Item -ItemType File -Path "services\domain\order_service.py" -Force
New-Item -ItemType File -Path "services\domain\license_service.py" -Force
New-Item -ItemType File -Path "services\domain\membership_service.py" -Force
New-Item -ItemType File -Path "services\domain\download_service.py" -Force

# core
New-Item -ItemType Directory -Path "services\core" -Force
New-Item -ItemType File -Path "services\core\__init__.py" -Force
New-Item -ItemType File -Path "services\core\purchase_flow.py" -Force
New-Item -ItemType File -Path "services\core\membership_flow.py" -Force
New-Item -ItemType File -Path "services\core\download_flow.py" -Force
```



### 创建 services/tests 总目录

```powershell
New-Item -ItemType Directory -Path "services\tests" -Force
New-Item -ItemType File -Path "services\tests\__init__.py" -Force
```



### 创建 factories

```powershell
New-Item -ItemType Directory -Path "services\tests\factories" -Force
New-Item -ItemType File -Path "services\tests\factories\__init__.py" -Force
New-Item -ItemType File -Path "services\tests\factories\user_factory.py" -Force
New-Item -ItemType File -Path "services\tests\factories\movie_factory.py" -Force
New-Item -ItemType File -Path "services\tests\factories\wallet_factory.py" -Force
New-Item -ItemType File -Path "services\tests\factories\order_factory.py" -Force
New-Item -ItemType File -Path "services\tests\factories\license_factory.py" -Force
New-Item -ItemType File -Path "services\tests\factories\membership_factory.py" -Force
New-Item -ItemType File -Path "services\tests\factories\download_factory.py" -Force
```



### 创建 Domain Service 单元测试目录

```powershell
New-Item -ItemType Directory -Path "services\tests\domain" -Force
New-Item -ItemType File -Path "services\tests\domain\__init__.py" -Force

New-Item -ItemType File -Path "services\tests\domain\test_movie_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_identity_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_user_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_wallet_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_order_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_license_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_membership_service.py" -Force
New-Item -ItemType File -Path "services\tests\domain\test_download_service.py" -Force
```



### 创建 Core Flow 单元测试目录

```powershell
New-Item -ItemType Directory -Path "services\tests\core" -Force
New-Item -ItemType File -Path "services\tests\core\__init__.py" -Force

New-Item -ItemType File -Path "services\tests\core\test_purchase_flow.py" -Force
New-Item -ItemType File -Path "services\tests\core\test_membership_flow.py" -Force
New-Item -ItemType File -Path "services\tests\core\test_download_flow.py" -Force
```



### 创建集成测试目录

```powershell
New-Item -ItemType Directory -Path "services\tests\integration" -Force
New-Item -ItemType File -Path "services\tests\integration\__init__.py" -Force

New-Item -ItemType File -Path "services\tests\integration\test_purchase_full_chain.py" -Force
New-Item -ItemType File -Path "services\tests\integration\test_membership_full_chain.py" -Force
```



## 测试顺序

### 总原则

1. **先测最底层、最确定、最常出事故的模块**：钱包（扣款/入账）
2. **再测闭环 Flow**：购买闭环、会员闭环、下载闭环
3. **最后补 CRUD 与查询**：电影/订单列表等（相对稳定）
4. **并发/锁测试放最后**：只对钱包与配额做少量关键并发测试
5. 每写一个测试文件就立刻跑：`python manage.py test services.tests...`



### 先写 factories（必须先有）

顺序：

1. `services/tests/factories/user_factory.py`
2. `services/tests/factories/wallet_factory.py`
3. `services/tests/factories/movie_factory.py`
4. `services/tests/factories/order_factory.py`
5. `services/tests/factories/license_factory.py`
6. `services/tests/factories/membership_factory.py`
7. `services/tests/factories/download_factory.py`

> 原则：后面的测试文件只调用 factory，不直接写 ORM create。



### 第一批：钱包 Domain

最关键、最容易写出高质量

文件：`services/tests/domain/test_wallet_service.py`

必须覆盖：

- `credit` 入账：余额变化正确 + CoinTransaction 写入正确
- `debit` 扣款：余额变化正确 + CoinTransaction 写入正确
- 余额不足：抛 `BalanceNotEnough`，余额不变，流水不新增
- ref_type/ref_id/operator/remark 的审计字段正确（管理员充值/扣减会用到）

> 这一步完成后，你已经具备“所有交易闭环的地基”。



### 第二批：授权 Domain

权限判断是所有业务入口

文件：`services/tests/domain/test_license_service.py`

必须覆盖：

- `grant_purchase_license`：创建成功
- 重复授权：抛 `BusinessRuleViolation`（并确保没有重复数据）
- `has_movie_access`：
    - 有购买授权 → True
    - 无购买授权但会员有效 → True
    - 都没有 → False

> 这一步完成后，下载/观看权限判断就稳定了。



### 第三批：购买闭环 Core

文件：`services/tests/core/test_purchase_flow.py`

必须覆盖（闭环一致性）：

- 成功购买：
    - 钱包扣款一次
    - 订单创建 + 状态 COMPLETED
    - 授权生成一次
    - CoinTransaction 的 ref 指向订单
- 失败回滚（关键）：
    - 人为制造授权发放失败（重复购买或 mock）
    - 断言：订单/流水/余额全部回滚（强一致）

> 这是你的系统主链路，优先级极高。



### 第四批：会员闭环 Core

文件：`services/tests/core/test_membership_flow.py`

必须覆盖：

- 开通会员：生成/更新 Membership，end_at 正确
- 未过期续费：从原 end_at 往后延长
- 已过期续费：从 now 开始（按你当前规则）
- 扣金币成功且流水正确（ref_type=MEMBERSHIP）

------



### 第五批：下载闭环 Core

文件：`services/tests/core/test_download_flow.py`

必须覆盖：

- 无权限：`PermissionDenied`
- 有权限：
    - can_download（配额允许）→ quota+1 → token 创建成功
    - token 校验（device_id 正确、未过期）
- token 过期 / device 不匹配：拒绝

------



### 第六批：订单 Domain

查询与状态流转

文件：`services/tests/domain/test_order_service.py`

覆盖：

- create_order 不扣款、不授权（只建订单+items）
- list/get 正常
- cancel/recalc_total_coin 正常
- set_status 合法性校验



### 第七批：用户/身份/电影等 CRUD

文件：

- `test_user_service.py`
- `test_identity_service.py`
- `test_movie_service.py`
- `test_membership_service.py`
- `test_download_service.py`（domain 层）

这些属于后台管理 CRUD，重要但不如闭环关键，放后面效率最高。



### 并发测试

并发测试会耗时、易不稳定，建议只做：

1. **钱包并发扣款**（TransactionTestCase）
    - 初始余额=10
    - 两线程同时扣 10
    - 结果：一个成功，一个失败，余额最终=0，流水只有 1 条
2. **下载配额并发增长**（TransactionTestCase）
    - 两线程同时 increase_daily_quota
    - 结果：count=2（不丢失）

> 并发测试只验证“锁是否真的生效”，不要写太多。







## 测试工厂

### 用户工厂

services/tests/factories/user_factory.py

```python
# services/tests/factories/user_factory.py
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from django.contrib.auth import get_user_model


@dataclass(frozen=True)
class UserCreateDTO:
    """
    测试用用户创建参数对象

    说明：
    - factories 里用 DTO 是为了让测试更清晰、可读、可维护
    - 你也可以不使用 DTO，直接传参，但 DTO 更适合中大型项目长期维护
    """
    username: str
    password: str
    email: str
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True


def _unique_username(prefix: str = "u") -> str:
    """
    生成唯一用户名，避免测试并发/重复运行时冲突
    """
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _unique_email(prefix: str = "u") -> str:
    """
    生成唯一邮箱，避免唯一约束冲突
    """
    return f"{prefix}_{uuid.uuid4().hex[:10]}@example.com"


def build_user_dto(
    *,
    username: Optional[str] = None,
    password: str = "TestPassw0rd!",
    email: Optional[str] = None,
    is_staff: bool = False,
    is_superuser: bool = False,
    is_active: bool = True,
) -> UserCreateDTO:
    """
    构建用户 DTO（仅用于测试）
    """
    return UserCreateDTO(
        username=username or _unique_username(),
        password=password,
        email=email or _unique_email(),
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
    )


def create_user(
    *,
    username: Optional[str] = None,
    password: str = "TestPassw0rd!",
    email: Optional[str] = None,
    is_active: bool = True,
    **extra_fields,
):
    """
    创建普通用户（测试工厂）

    参数：
    - username/email 可不传，自动生成唯一值
    - password 默认可用
    - extra_fields 用于兼容自定义 User 模型的额外字段（如 phone/nickname 等）
    """
    User = get_user_model()
    dto = build_user_dto(
        username=username,
        password=password,
        email=email,
        is_active=is_active,
    )

    # create_user 会自动处理密码哈希
    user = User.objects.create_user(
        username=dto.username,
        email=dto.email,
        password=dto.password,
        **extra_fields,
    )

    # Django 默认 create_user 会让 is_active=True，这里按入参强制覆盖
    if hasattr(user, "is_active") and user.is_active != dto.is_active:
        user.is_active = dto.is_active
        user.save(update_fields=["is_active"])

    return user


def create_admin(
    *,
    username: Optional[str] = None,
    password: str = "AdminPassw0rd!",
    email: Optional[str] = None,
    is_active: bool = True,
    **extra_fields,
):
    """
    创建管理员用户（测试工厂）
    - 用于模拟后台管理端 operator
    """
    User = get_user_model()
    dto = build_user_dto(
        username=username or _unique_username("admin"),
        password=password,
        email=email or _unique_email("admin"),
        is_staff=True,
        is_superuser=True,
        is_active=is_active,
    )

    # create_superuser 会自动处理密码、is_staff、is_superuser
    user = User.objects.create_superuser(
        username=dto.username,
        email=dto.email,
        password=dto.password,
        **extra_fields,
    )

    # 强制状态一致
    updates = []
    if hasattr(user, "is_active") and user.is_active != dto.is_active:
        user.is_active = dto.is_active
        updates.append("is_active")

    if hasattr(user, "is_staff") and not user.is_staff:
        user.is_staff = True
        updates.append("is_staff")

    if hasattr(user, "is_superuser") and not user.is_superuser:
        user.is_superuser = True
        updates.append("is_superuser")

    if updates:
        user.save(update_fields=updates)

    return user
```



### 钱包测试工厂

services/tests/factories/wallet_factory.py

```python
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
```



### 电影测试工厂

services/tests/factories/movie_factory.py

```python
# services/tests/factories/movie_factory.py
from __future__ import annotations

import uuid
from typing import Optional

from apps.content.models import Movie


def _unique_title(prefix: str = "测试电影") -> str:
    """
    生成唯一电影标题，避免测试中唯一约束冲突
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_movie(
    *,
    title: Optional[str] = None,
    price_coin: int = 10,
    status: str | None = None,
    year: int = 2025,
    is_active: bool = True,
    **extra_fields,
) -> Movie:
    """
    创建电影（测试工厂）

    设计目标：
    - 创建一条“合法、可购买”的电影记录
    - 默认状态：可售 / 上架
    - 供订单 / 授权 / 下载测试使用

    参数说明：
    - title: 电影标题（不传则自动生成唯一值）
    - price_coin: 电影金币价格
    - status: 电影状态（不传则使用模型默认）
    - year: 上映年份
    - is_active: 是否有效（软删除/上下架场景）
    - extra_fields: 兼容模型未来扩展字段
    """
    if price_coin <= 0:
        raise ValueError("price_coin 必须大于 0")

    data = {
        "title": title or _unique_title(),
        "price_coin": price_coin,
        "year": year,
        "is_active": is_active,
    }

    if status is not None:
        data["status"] = status

    data.update(extra_fields)

    movie = Movie.objects.create(**data)
    return movie


def create_onsale_movie(
    *,
    title: Optional[str] = None,
    price_coin: int = 10,
    **extra_fields,
) -> Movie:
    """
    创建“已上架/可售”的电影（语义化快捷方法）
    """
    return create_movie(
        title=title,
        price_coin=price_coin,
        status=Movie.Status.ONSALE,
        **extra_fields,
    )


def create_offline_movie(
    *,
    title: Optional[str] = None,
    price_coin: int = 10,
    **extra_fields,
) -> Movie:
    """
    创建“下架”的电影（用于异常/边界测试）
    """
    return create_movie(
        title=title,
        price_coin=price_coin,
        status=Movie.Status.OFFLINE,
        **extra_fields,
    )
```



### 订单测试工厂

services/tests/factories/order_factory.py

```python
# services/tests/factories/order_factory.py
from __future__ import annotations

from typing import Iterable, List

from apps.orders.models import PurchaseOrder, PurchaseOrderItem
from services.domain.order_service import OrderItemCreateDTO, OrderService


def create_order(
    *,
    user,
    movies: Iterable,
    price_coin_map: dict | None = None,
    remark: str | None = None,
) -> PurchaseOrder:
    """
    创建订单（测试工厂，不扣款、不授权）

    参数说明：
    - user: 下单用户
    - movies: 电影对象列表（Iterable[Movie]）
    - price_coin_map:
        - 可选，用于指定每个电影的价格
        - 例如 {movie1.id: 10, movie2.id: 20}
        - 不传则默认每个 movie.price_coin
    - remark: 订单备注（测试用）

    返回：
    - PurchaseOrder（状态：CREATED）
    """
    movies = list(movies)
    if not movies:
        raise ValueError("movies 不能为空")

    items: List[OrderItemCreateDTO] = []

    for movie in movies:
        if not getattr(movie, "id", None):
            raise ValueError("movie 必须是已保存对象")

        price = (
            price_coin_map.get(movie.id)
            if price_coin_map
            else getattr(movie, "price_coin", None)
        )
        if price is None:
            raise ValueError("无法确定 movie 的 price_coin")

        items.append(
            OrderItemCreateDTO(
                movie=movie,
                price_coin=price,
            )
        )

    order = OrderService.create_order(
        user=user,
        items=items,
        remark=remark or "测试订单",
    )
    return order


def create_single_movie_order(
    *,
    user,
    movie,
    price_coin: int | None = None,
) -> PurchaseOrder:
    """
    创建单电影订单（语义化快捷方法）
    """
    return create_order(
        user=user,
        movies=[movie],
        price_coin_map={movie.id: price_coin}
        if price_coin is not None
        else None,
    )


def create_multi_movie_order(
    *,
    user,
    movies: Iterable,
) -> PurchaseOrder:
    """
    创建多电影订单（用于测试批量购买 / 边界情况）
    """
    return create_order(
        user=user,
        movies=movies,
    )


def mark_order_completed(order: PurchaseOrder) -> PurchaseOrder:
    """
    将订单标记为已完成（测试辅助）

    ⚠️ 注意：
    - 这是“测试捷径”
    - 正常业务中应由 PurchaseFlow 更新状态
    """
    order.status = PurchaseOrder.Status.COMPLETED
    order.save(update_fields=["status"])
    return order


def get_order_items(order: PurchaseOrder):
    """
    获取订单明细列表（测试辅助）
    """
    return PurchaseOrderItem.objects.filter(order=order).select_related("movie")
```



### 权限测试工厂

services/tests/factories/license_factory.py

```python
# services/tests/factories/license_factory.py
from __future__ import annotations

from typing import Optional

from apps.orders.models import PurchaseLicense
from services.domain.license_service import LicenseService


def create_purchase_license(
    *,
    user,
    movie,
    order_item=None,
) -> PurchaseLicense:
    """
    创建用户购买电影的授权记录（测试工厂）

    参数：
    - user: 关联的用户对象
    - movie: 关联的电影对象
    - order_item: 关联的订单条目（如果有）

    返回：
    - 创建的 PurchaseLicense 对象
    """
    # 如果没有提供 order_item，模拟通过订单购买产生授权
    if not order_item:
        from services.tests.factories.order_factory import create_order
        order = create_order(user=user, movies=[movie])
        order_item = order.items.first()

    return LicenseService.grant_purchase_license(
        user=user,
        movie=movie,
        order_item=order_item,
    )


def create_force_license(
    *,
    user,
    movie,
    operator=None,
    remark=None,
) -> PurchaseLicense:
    """
    创建强制发放的授权记录（用于补偿/特殊场景）
    - 强制授权不需要订单项，可以通过虚拟订单或其他方式处理

    参数：
    - user: 关联的用户对象
    - movie: 关联的电影对象
    - operator: 操作员（可选，默认为 None）
    - remark: 备注信息（可选）

    返回：
    - 创建的 PurchaseLicense 对象
    """
    return LicenseService.grant_license_force(
        user=user,
        movie=movie,
        operator=operator,
        remark=remark,
    )
```



### 会员测试工厂

services/tests/factories/membership_factory.py

```python
# services/tests/factories/membership_factory.py
from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.membership.models import Membership


def create_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    status: str = Membership.Status.ACTIVE,
    start_at=None,
    end_at=None,
) -> Membership:
    """
    创建会员记录（测试工厂，底层方法）

    参数：
    - user: 用户对象（必传）
    - plan: Membership.Plan.MONTH / YEAR
    - status: Membership.Status.ACTIVE / EXPIRED / GRACE
    - start_at / end_at: 可手动指定时间区间
    """
    now = timezone.now()

    if start_at is None:
        start_at = now

    if end_at is None:
        # 默认：一个月有效期
        end_at = start_at + timedelta(days=30)

    return Membership.objects.create(
        user=user,
        plan=plan,
        status=status,
        start_at=start_at,
        end_at=end_at,
    )


# =============================
# 语义化快捷方法（强烈推荐在测试中使用）
# =============================

def create_active_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    days: int = 30,
) -> Membership:
    """
    创建当前有效的会员
    """
    now = timezone.now()
    return create_membership(
        user=user,
        plan=plan,
        status=Membership.Status.ACTIVE,
        start_at=now - timedelta(days=1),
        end_at=now + timedelta(days=days),
    )


def create_expired_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    days_ago: int = 1,
) -> Membership:
    """
    创建已过期会员
    """
    now = timezone.now()
    return create_membership(
        user=user,
        plan=plan,
        status=Membership.Status.EXPIRED,
        start_at=now - timedelta(days=30 + days_ago),
        end_at=now - timedelta(days=days_ago),
    )


def create_grace_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    grace_days: int = 3,
) -> Membership:
    """
    创建宽限期会员（例如：刚过期但仍允许访问）
    """
    now = timezone.now()
    return create_membership(
        user=user,
        plan=plan,
        status=Membership.Status.GRACE,
        start_at=now - timedelta(days=30),
        end_at=now - timedelta(days=1),
    )
```



### 下载测试工厂

services/tests/factories/download_factory.py

```python
# services/tests/factories/download_factory.py
from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.download.models import DownloadToken, DownloadQuota


def create_download_token(
    *,
    user,
    movie,
    device_id: str = "test-device",
    expires_minutes: int = 10,
) -> DownloadToken:
    """
    创建下载 Token（测试工厂）

    参数：
    - user: 用户对象
    - movie: 电影对象
    - device_id: 设备标识
    - expires_minutes: 多少分钟后过期

    注意：
    - factory 不做任何权限判断
    - token 是否有效应由 DownloadService / DownloadFlow 测试
    """
    expires_at = timezone.now() + timedelta(minutes=expires_minutes)

    return DownloadToken.objects.create(
        user=user,
        movie=movie,
        device_id=device_id,
        expires_at=expires_at,
    )


def create_expired_download_token(
    *,
    user,
    movie,
    device_id: str = "test-device",
    expired_minutes_ago: int = 5,
) -> DownloadToken:
    """
    创建已过期的下载 Token（用于异常测试）
    """
    expires_at = timezone.now() - timedelta(minutes=expired_minutes_ago)

    return DownloadToken.objects.create(
        user=user,
        movie=movie,
        device_id=device_id,
        expires_at=expires_at,
    )


def create_download_quota(
    *,
    user,
    movie,
    date=None,
    count: int = 0,
) -> DownloadQuota:
    """
    创建下载配额记录（测试工厂）

    参数：
    - user: 用户对象
    - movie: 电影对象
    - date: 日期（默认今天）
    - count: 已下载次数
    """
    if date is None:
        date = timezone.localdate()

    return DownloadQuota.objects.create(
        user=user,
        movie=movie,
        date=date,
        count=count,
    )


def reset_download_data(
    *,
    user,
    movie=None,
):
    """
    重置下载相关数据（测试辅助）

    使用场景：
    - 多个测试共用同一 user/movie
    - 确保配额/token 干净

    参数：
    - user: 用户对象（必传）
    - movie: 电影对象（可选，不传则清空该用户所有下载数据）
    """
    token_qs = DownloadToken.objects.filter(user=user)
    quota_qs = DownloadQuota.objects.filter(user=user)

    if movie is not None:
        token_qs = token_qs.filter(movie=movie)
        quota_qs = quota_qs.filter(movie=movie)

    token_qs.delete()
    quota_qs.delete()
```



## 测试钱包 Domain

最关键、最容易写出高质量

文件：

services/tests/domain/test_wallet_service.py

```python
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
```



必须覆盖：

- `credit` 入账：余额变化正确 + CoinTransaction 写入正确
- `debit` 扣款：余额变化正确 + CoinTransaction 写入正确
- 余额不足：抛 `BalanceNotEnough`，余额不变，流水不新增
- ref_type/ref_id/operator/remark 的审计字段正确（管理员充值/扣减会用到）



执行测试：

```bash
python manage.py test services.tests.domain.test_wallet_service
```





## 测试授权 Domain

权限判断是所有业务入口

文件：

services/tests/domain/test_license_service.py

```python
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
```



必须覆盖：

- `grant_purchase_license`：创建成功
- 重复授权：抛 `BusinessRuleViolation`（并确保没有重复数据）
- `has_movie_access`：
    - 有购买授权 → True
    - 无购买授权但会员有效 → True
    - 都没有 → False



执行测试：

```bash
python manage.py test services.tests.domain.test_license_service
```





### 第三批：购买闭环 Core

文件：`services/tests/core/test_purchase_flow.py`

必须覆盖（闭环一致性）：

- 成功购买：
    - 钱包扣款一次
    - 订单创建 + 状态 COMPLETED
    - 授权生成一次
    - CoinTransaction 的 ref 指向订单
- 失败回滚（关键）：
    - 人为制造授权发放失败（重复购买或 mock）
    - 断言：订单/流水/余额全部回滚（强一致）

> 这是你的系统主链路，优先级极高。



### 第四批：会员闭环 Core

文件：`services/tests/core/test_membership_flow.py`

必须覆盖：

- 开通会员：生成/更新 Membership，end_at 正确
- 未过期续费：从原 end_at 往后延长
- 已过期续费：从 now 开始（按你当前规则）
- 扣金币成功且流水正确（ref_type=MEMBERSHIP）

------



### 第五批：下载闭环 Core

文件：`services/tests/core/test_download_flow.py`

必须覆盖：

- 无权限：`PermissionDenied`
- 有权限：
    - can_download（配额允许）→ quota+1 → token 创建成功
    - token 校验（device_id 正确、未过期）
- token 过期 / device 不匹配：拒绝

------



### 第六批：订单 Domain

查询与状态流转

文件：`services/tests/domain/test_order_service.py`

覆盖：

- create_order 不扣款、不授权（只建订单+items）
- list/get 正常
- cancel/recalc_total_coin 正常
- set_status 合法性校验



### 第七批：用户/身份/电影等 CRUD

文件：

- `test_user_service.py`
- `test_identity_service.py`
- `test_movie_service.py`
- `test_membership_service.py`
- `test_download_service.py`（domain 层）

这些属于后台管理 CRUD，重要但不如闭环关键，放后面效率最高。



### 并发测试

并发测试会耗时、易不稳定，建议只做：

1. **钱包并发扣款**（TransactionTestCase）
    - 初始余额=10
    - 两线程同时扣 10
    - 结果：一个成功，一个失败，余额最终=0，流水只有 1 条
2. **下载配额并发增长**（TransactionTestCase）
    - 两线程同时 increase_daily_quota
    - 结果：count=2（不丢失）

> 并发测试只验证“锁是否真的生效”，不要写太多。