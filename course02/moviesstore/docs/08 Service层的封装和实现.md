# 08 Service层的封装和实现



## 一、Service 层的定位与设计原则

### 1.1 Service 层的核心定位

Service 层是**系统唯一可信的业务执行层**，负责：

- 承载所有 **业务规则**
- 控制所有 **数据库写操作**
- 作为后台管理系统、Web/App 端的**统一业务入口**

任何业务，只允许通过 Service 层进入数据库。



### 1.2 强制工程约束（不可违反）

1. 禁止在以下位置编写业务逻辑
    - Model
    - Serializer
    - View / API
    - signals
2. 所有 `create / update / delete / 状态流转` 必须在 Service 中完成
3. 涉及多表写操作，必须由 Service 控制事务
4. Service 不依赖 HTTP、不返回 Response
5. 后台管理系统、App/Web 端 **共用同一套 Service**



## 二、Service 层总体架构划分

### 2.1 双层 Service 架构（核心）

Service 层必须同时具备两类能力：

1. **CRUD / 管理型 Service**
    - 提供后台管理系统所需的增删改查、上下架、启停用等能力
2. **Core Flow Service（闭环）**
    - 提供交易、会员、下载等强一致业务闭环



### 2.2 Service 目录结构

```text
services/
├── common/
│   ├── exceptions.py
│   └── base.py
├── domain/
│   ├── movie_service.py
│   ├── identity_service.py
│   ├── user_service.py
│   ├── wallet_service.py
│   ├── order_service.py
│   ├── license_service.py
│   ├── membership_service.py
│   └── download_service.py
└── core/
    ├── purchase_flow.py
    ├── membership_flow.py
    └── download_flow.py
```



创建目录结构（PowerShell）

```powershell
# services 根目录
New-Item -ItemType Directory -Path "services" -Force

# 一级子目录
New-Item -ItemType Directory -Path "services\common" -Force
New-Item -ItemType Directory -Path "services\domain" -Force
New-Item -ItemType Directory -Path "services\core" -Force
```



创建 common 目录文件

```powershell
New-Item -ItemType File -Path "services\common\__init__.py" -Force
New-Item -ItemType File -Path "services\common\exceptions.py" -Force
New-Item -ItemType File -Path "services\common\base.py" -Force
```



创建 domain 目录文件

```powershell
New-Item -ItemType File -Path "services\domain\__init__.py" -Force
New-Item -ItemType File -Path "services\domain\movie_service.py" -Force
New-Item -ItemType File -Path "services\domain\identity_service.py" -Force
New-Item -ItemType File -Path "services\domain\user_service.py" -Force
New-Item -ItemType File -Path "services\domain\wallet_service.py" -Force
New-Item -ItemType File -Path "services\domain\order_service.py" -Force
New-Item -ItemType File -Path "services\domain\license_service.py" -Force
New-Item -ItemType File -Path "services\domain\membership_service.py" -Force
New-Item -ItemType File -Path "services\domain\download_service.py" -Force
```



创建 core 目录文件

```powershell
New-Item -ItemType File -Path "services\core\__init__.py" -Force
New-Item -ItemType File -Path "services\core\purchase_flow.py" -Force
New-Item -ItemType File -Path "services\core\membership_flow.py" -Force
New-Item -ItemType File -Path "services\core\download_flow.py" -Force
```



## 三、Service 基础设施

### 3.1 基础事务封装

services/common/base.py

```python
from django.db import transaction


class BaseService:
    """
    所有 Service 的基础类
    """

    @classmethod
    def atomic(cls):
        return transaction.atomic()
```



### 3.2 统一异常体系

services/common/exceptions.py

```python
class ServiceError(Exception):
    pass


class NotFound(ServiceError):
    pass


class PermissionDenied(ServiceError):
    pass


class BalanceNotEnough(ServiceError):
    pass


class BusinessRuleViolation(ServiceError):
    pass
```



## 四、内容域 Service

### 4.1 MovieService 职责

- 创建 / 编辑电影
- 上架 / 下架 / 草稿状态流转
- 管理电影封面与资源
- 提供后台与前台查询能力



### 4.2 MovieService 实现

services/domain/movie_service.py

```python
from apps.content.models import Movie, MovieAsset
from services.common.exceptions import NotFound


class MovieService:

    @staticmethod
    def create_movie(data: dict) -> Movie:
        return Movie.objects.create(**data)

    @staticmethod
    def update_movie(movie_id: int, data: dict) -> Movie:
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            raise NotFound("电影不存在")
        for k, v in data.items():
            setattr(movie, k, v)
        movie.save()
        return movie

    @staticmethod
    def set_status(movie_id: int, status: str):
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            raise NotFound("电影不存在")
        movie.status = status
        movie.save(update_fields=["status"])

    @staticmethod
    def add_asset(movie: Movie, asset_type: str, url: str, is_primary=False):
        if is_primary:
            MovieAsset.objects.filter(movie=movie, asset_type=asset_type).update(is_primary=False)
        return MovieAsset.objects.create(
            movie=movie,
            asset_type=asset_type,
            url=url,
            is_primary=is_primary,
        )
```



## 五、账号域 Service

### 5.1 IdentityService 职责

- 绑定 / 解绑 邮箱、手机号、用户名
- 设置主身份
- 标记验证状态（验证码通过后）



services/domain/identity_service.py

```python
from apps.movie_auth.models import UserIdentity
from services.common.exceptions import BusinessRuleViolation


class IdentityService:

    @staticmethod
    def bind_identity(user, identity_type, identifier):
        exists = UserIdentity.objects.filter(
            identity_type=identity_type,
            identifier=identifier
        ).exists()
        if exists:
            raise BusinessRuleViolation("该身份已被占用")
        return UserIdentity.objects.create(
            user=user,
            identity_type=identity_type,
            identifier=identifier,
        )
```



## 六、钱包 Service

### 6.1 WalletService 职责

- 创建钱包
- 查询余额
- 金币入账 / 扣减（统一入口）
- 并发安全（行级锁）



services/domain/wallet_service.py

```python
from django.db import transaction
from django.utils import timezone

from apps.wallet.models import Wallet, CoinTransaction
from services.common.exceptions import BalanceNotEnough, NotFound


class WalletService:

    @staticmethod
    def get_or_create(user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet

    @staticmethod
    @transaction.atomic
    def credit(user, amount, tx_type, ref_type, ref_id, operator=None, remark=None):
        wallet = Wallet.objects.select_for_update().filter(user=user).first()
        if not wallet:
            raise NotFound("钱包不存在")
        wallet.balance += amount
        wallet.updated_at = timezone.now()
        wallet.save(update_fields=["balance", "updated_at"])

        CoinTransaction.objects.create(
            user=user,
            operator=operator,
            change_amount=amount,
            balance_after=wallet.balance,
            type=tx_type,
            ref_type=ref_type,
            ref_id=ref_id,
            remark=remark,
        )

    @staticmethod
    @transaction.atomic
    def debit(user, amount, tx_type, ref_type, ref_id, operator=None, remark=None):
        wallet = Wallet.objects.select_for_update().filter(user=user).first()
        if wallet.balance < amount:
            raise BalanceNotEnough("余额不足")
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])
        CoinTransaction.objects.create(
            user=user,
            operator=operator,
            change_amount=-amount,
            balance_after=wallet.balance,
            type=tx_type,
            ref_type=ref_type,
            ref_id=ref_id,
            remark=remark,
        )
```



## 七、订单 + 授权

### 7.1 购买闭环职责

- 校验价格
- 钱包扣款
- 订单创建
- 授权生成
- 状态一致性保证



services/core/purchase_flow.py

```python
from django.db import transaction
from services.domain.wallet_service import WalletService
from services.domain.license_service import LicenseService
from apps.orders.models import PurchaseOrder, PurchaseOrderItem


class PurchaseFlow:

    @staticmethod
    @transaction.atomic
    def purchase_movie(user, movie):
        order = PurchaseOrder.objects.create(
            user=user,
            total_coin=movie.price_coin,
        )

        item = PurchaseOrderItem.objects.create(
            order=order,
            movie=movie,
            price_coin=movie.price_coin,
        )

        WalletService.debit(
            user=user,
            amount=movie.price_coin,
            tx_type="PURCHASE",
            ref_type="ORDER",
            ref_id=order.id,
        )

        LicenseService.grant_purchase_license(
            user=user,
            movie=movie,
            order_item=item,
        )

        order.status = PurchaseOrder.Status.COMPLETED
        order.save(update_fields=["status"])

        return order
```



## 八、下载 Core Flow

### 8.1 DownloadFlow 职责

- 校验是否有权限
- 校验下载次数
- 生成下载 Token



services/core/download_flow.py

```python
from datetime import timedelta
from django.utils import timezone

from services.domain.license_service import LicenseService
from services.domain.download_service import DownloadService
from services.common.exceptions import PermissionDenied


class DownloadFlow:

    @staticmethod
    def create_download_token(user, movie, device_id):
        if not LicenseService.has_movie_access(user, movie):
            raise PermissionDenied("无下载权限")

        return DownloadService.create_token(
            user=user,
            movie=movie,
            device_id=device_id,
            expires_at=timezone.now() + timedelta(minutes=10),
        )
```

