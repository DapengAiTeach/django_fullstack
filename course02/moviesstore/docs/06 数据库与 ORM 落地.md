# 06 数据库与 ORM 落地



## 一、Admin UI 框架配置

### 1.1 安装依赖

```bash
pip install django-jazzmin==2.6.0
```



### 1.2 settings.py 注册

```python
INSTALLED_APPS = [
    # Admin UI（必须在 django.contrib.admin 之前）
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "apps.movie_auth",
    "apps.accounts",
    "apps.content",
    "apps.wallet",
    "apps.payment",
    "apps.orders",
    "apps.membership",
    "apps.download",
]
```



### 1.3 Jazzmin 基础配置

```python
JAZZMIN_SETTINGS = {
    "site_title": "电影商城后台",
    "site_header": "数字电影商城",
    "site_brand": "MovieStore Admin",
    "welcome_sign": "欢迎进入数字电影商城管理后台",
    "copyright": "大鹏AI教育",

    "search_model": [
        "content.Movie",
        "movie_auth.UserIdentity",
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "accounts": "fas fa-user",
        "content": "fas fa-film",
        "wallet": "fas fa-wallet",
        "orders": "fas fa-shopping-cart",
        "membership": "fas fa-id-card",
        "download": "fas fa-download",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
}
```



## 二、认证域

apps/movie_auth

### 2.1 models.py

```python
from django.db import models
from django.conf import settings


class UserIdentity(models.Model):
    """
    用户登录身份表
    用于支持：用户名 / 邮箱 / 手机号 多种登录方式
    """

    class IdentityType(models.TextChoices):
        USERNAME = "USERNAME", "用户名"
        EMAIL = "EMAIL", "邮箱"
        PHONE = "PHONE", "手机号"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    identity_type = models.CharField(
        max_length=20,
        choices=IdentityType.choices,
        verbose_name="身份类型",
    )
    identifier = models.CharField(
        max_length=255,
        verbose_name="登录标识",
        help_text="用户名 / 邮箱 / 手机号",
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="是否主身份",
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name="是否已验证",
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
        db_table = "user_identity"
        verbose_name = "用户登录身份"
        verbose_name_plural = "用户登录身份"
        unique_together = ("identity_type", "identifier")

    def __str__(self):
        return f"{self.identity_type} - {self.identifier}"
```



### 2.2 admin.py

```python
from django.contrib import admin
from .models import UserIdentity


@admin.register(UserIdentity)
class UserIdentityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "identity_type",
        "identifier",
        "is_primary",
        "is_verified",
        "created_at",
    )
    list_filter = ("identity_type", "is_verified")
    search_fields = ("identifier",)
```



## 三、内容域

内容域是后台使用最频繁的模块，这里给出**完整标准实现**

apps/content



### 3.1 models.py

```python
from django.db import models


class Movie(models.Model):
    """
    电影基础信息（商城维度）
    """

    class AccessType(models.TextChoices):
        FREE = "FREE", "免费"
        BUY_ONLY = "BUY_ONLY", "仅购买"
        BUY_OR_VIP = "BUY_OR_VIP", "购买或会员"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "草稿"
        ONLINE = "ONLINE", "上架"
        OFFLINE = "OFFLINE", "下架"

    title = models.CharField(
        max_length=255,
        verbose_name="电影名称",
    )
    original_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="原片名",
    )
    release_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="上映年份",
    )

    access_type = models.CharField(
        max_length=20,
        choices=AccessType.choices,
        verbose_name="观看方式",
    )
    price_coin = models.BigIntegerField(
        default=0,
        verbose_name="价格（金豆）",
        help_text="0 表示免费",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="状态",
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="上架时间",
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
        db_table = "movie"
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self):
        return self.title
```



### 3.2 MovieDetail

```python
class MovieDetail(models.Model):
    """
    电影详情（内容维度）
    """

    movie = models.OneToOneField(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    synopsis = models.TextField(
        verbose_name="剧情简介",
    )
    duration_minutes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="片长（分钟）",
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
        db_table = "movie_detail"
        verbose_name = "电影详情"
        verbose_name_plural = "电影详情"
```



### 3.3 MovieAsset

```python
class MovieAsset(models.Model):
    """
    电影资源（封面 / 视频 / 海报）
    """

    class AssetType(models.TextChoices):
        COVER = "COVER", "封面"
        VIDEO = "VIDEO", "视频"
        POSTER = "POSTER", "海报"

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        verbose_name="资源类型",
    )
    asset_url = models.CharField(
        max_length=500,
        verbose_name="资源地址",
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="是否主资源",
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name="排序值",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "movie_asset"
        verbose_name = "电影资源"
        verbose_name_plural = "电影资源"
```



### 3.4 forms.py

后台表单

```python
from django import forms
from .models import Movie


class MovieAdminForm(forms.ModelForm):
    """
    后台电影表单
    """

    class Meta:
        model = Movie
        fields = "__all__"

    def clean_price_coin(self):
        price = self.cleaned_data["price_coin"]
        if price < 0:
            raise forms.ValidationError("价格不能为负数")
        return price
```



### 3.5 admin.py

Inline + 表单

```python
from django.contrib import admin
from .models import Movie, MovieDetail, MovieAsset
from .forms import MovieAdminForm


class MovieDetailInline(admin.StackedInline):
    model = MovieDetail
    extra = 0


class MovieAssetInline(admin.TabularInline):
    model = MovieAsset
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm

    list_display = (
        "id",
        "title",
        "access_type",
        "price_coin",
        "status",
        "published_at",
    )
    list_filter = ("status", "access_type")
    search_fields = ("title",)

    inlines = [
        MovieDetailInline,
        MovieAssetInline,
    ]
```



下面是我按你新要求**重写后的“第四章及之后的完整内容”**（可直接复制落地），并且**把“管理员给用户充值金币”作为一等公民能力**来设计与实现。

你会得到：

- 钱包模块：**管理员充值/扣减金币**（后台直接操作，带备注、带操作者、事务安全、自动写流水）
- 订单模块：后台只读（防篡改交易事实）
- 会员模块：后台只读（生命周期由系统控制）
- 下载模块：后台只读（审计与排查）

> 说明：为了让“管理员充值/扣减”在审计上成立，**需要给 CoinTransaction 增加“操作人 operator + 备注 remark”字段**，并扩展流水类型枚举。
> 这属于真实项目必备能力（否则无法追责与审计）。

------

# 四、钱包模块

## 4.1 设计目标与约束

钱包模块负责金币资产的**安全与可审计**：

- Wallet：余额快照（1 用户 1 钱包）
- CoinTransaction：不可变账本（所有变更必须写流水）



重要能力：

- 管理员可在后台对用户进行：
    - **充值金币（增加）**
    - **扣减金币（减少）**
- 每次操作必须记录：
    - 操作人（管理员）
    - 备注（原因）
    - 变动前后余额（由系统写入）



硬性约束：

1. **后台禁止直接编辑 Wallet.balance**（必须走“管理员充值/扣减”入口）
2. **CoinTransaction 禁止后台新增/修改/删除**（账本不可篡改）
3. 管理员扣减不允许扣成负数（余额不足直接拒绝）



## 4.2 models.py

apps/wallet/models.py

```python
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
```



## 4.3 forms.py

管理员充值/扣减表单 apps/wallet/forms.py

```python
from django import forms


class AdminCoinAdjustForm(forms.Form):
    """
    管理员金币调整表单（后台入口使用）
    - amount：正整数
    - action：充值 or 扣减
    - remark：原因（必填）
    """

    ACTION_RECHARGE = "RECHARGE"
    ACTION_DEDUCT = "DEDUCT"

    action = forms.ChoiceField(
        label="操作类型",
        choices=(
            (ACTION_RECHARGE, "充值金币（增加）"),
            (ACTION_DEDUCT, "扣减金币（减少）"),
        ),
        required=True,
    )

    amount = forms.IntegerField(
        label="金币数量",
        min_value=1,
        help_text="必须为正整数",
        required=True,
    )

    remark = forms.CharField(
        label="备注（原因）",
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="必须填写操作原因，便于审计追责",
    )
```



## 4.4 admin.py

完整：列表、只读、充值/扣减入口、事务安全

apps/wallet/admin.py

```python
# apps/movie_auth/models.py
from django.conf import settings
from django.db import models


class UserIdentity(models.Model):
    """
    用户登录身份表（账号体系核心）
    目的：
    1. 支持多种登录标识：用户名/邮箱/手机号
    2. 允许一个用户绑定多个身份（例如：用户名 + 邮箱 + 手机号）
    3. 数据库层保证同一标识不被多个用户重复占用（唯一约束）

    注意（MySQL utf8mb4 索引限制）：
    - identifier 会参与唯一约束，因此 max_length 不能用 255
    - 为避免 1071（key too long），统一使用 191
    """

    class IdentityType(models.TextChoices):
        USERNAME = "USERNAME", "用户名"
        EMAIL = "EMAIL", "邮箱"
        PHONE = "PHONE", "手机号"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
        related_name="identities",
    )

    identity_type = models.CharField(
        max_length=20,
        choices=IdentityType.choices,
        verbose_name="身份类型",
        help_text="用户名/邮箱/手机号",
    )

    identifier = models.CharField(
        max_length=191,  # 关键：参与唯一索引，避免 utf8mb4 下索引过长
        verbose_name="登录标识",
        help_text="用户名 / 邮箱 / 手机号",
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="是否主身份",
        help_text="主身份用于默认展示与主登录方式标记",
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="是否已验证",
        help_text="邮箱/手机号验证码校验通过后置为 True",
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
        db_table = "user_identity"
        verbose_name = "用户登录身份"
        verbose_name_plural = "用户登录身份"

        # 同一标识（如同一个手机号）不能被多个用户占用
        # identity_type + identifier 联合唯一
        unique_together = ("identity_type", "identifier")

        indexes = [
            models.Index(fields=["user"], name="idx_identity_user"),
            models.Index(fields=["identity_type", "identifier"], name="idx_identity_lookup"),
        ]

    def __str__(self) -> str:
        return f"{self.get_identity_type_display()} - {self.identifier}"


class OAuthAccount(models.Model):
    """
    第三方登录绑定表
    支持：微信、QQ（可扩展更多 Provider）
    目的：
    - 同一第三方账号只能绑定一个站内用户（唯一约束）
    - 允许一个站内用户绑定多个第三方账号
    """

    class Provider(models.TextChoices):
        WECHAT = "WECHAT", "微信"
        QQ = "QQ", "QQ"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
        related_name="oauth_accounts",
    )

    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
        verbose_name="第三方平台",
    )

    # open_id / union_id 都可能参与唯一约束：长度必须控制（191 安全）
    open_id = models.CharField(
        max_length=191,
        null=True,
        blank=True,
        verbose_name="OpenID",
        help_text="第三方平台用户唯一标识（可能为空）",
    )

    union_id = models.CharField(
        max_length=191,
        null=True,
        blank=True,
        verbose_name="UnionID",
        help_text="跨应用统一标识（可能为空）",
    )

    nickname = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="昵称",
    )

    avatar_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="头像地址",
    )

    last_login_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="最近登录时间",
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
        db_table = "oauth_account"
        verbose_name = "第三方账号绑定"
        verbose_name_plural = "第三方账号绑定"

        # 注意：MySQL 唯一约束允许多个 NULL，因此 open_id/union_id 为空时不会互相冲突
        constraints = [
            models.UniqueConstraint(fields=["provider", "open_id"], name="uniq_provider_openid"),
            models.UniqueConstraint(fields=["provider", "union_id"], name="uniq_provider_unionid"),
        ]

        indexes = [
            models.Index(fields=["user"], name="idx_oauth_user"),
            models.Index(fields=["provider"], name="idx_oauth_provider"),
        ]

    def __str__(self) -> str:
        return f"{self.get_provider_display()} - user:{self.user_id}"


class AuthOTP(models.Model):
    """
    登录/注册/找回密码验证码表
    用于支持：
    - 账户/邮箱/手机号 + 验证码登录
    - MFA（二次校验）预留
    - 注册/找回密码验证码

    关键点：
    - 只存 code_hash，不存明文验证码（安全要求）
    - receiver 会参与联合索引，为避免 1071，使用 191
    """

    class Purpose(models.TextChoices):
        LOGIN = "LOGIN", "登录"
        MFA = "MFA", "二次验证"
        REGISTER = "REGISTER", "注册"
        RESET_PASSWORD = "RESET_PASSWORD", "找回密码"

    purpose = models.CharField(
        max_length=30,
        choices=Purpose.choices,
        verbose_name="用途",
    )

    channel = models.CharField(
        max_length=20,
        verbose_name="发送渠道",
        help_text="例如：SMS / EMAIL",
    )

    receiver = models.CharField(
        max_length=191,  # 关键：参与索引，避免 utf8mb4 下联合索引过长
        verbose_name="接收方",
        help_text="邮箱/手机号等接收地址",
    )

    code_hash = models.CharField(
        max_length=255,
        verbose_name="验证码哈希",
        help_text="只保存验证码哈希值，不保存明文",
    )

    expires_at = models.DateTimeField(
        verbose_name="过期时间",
    )

    consumed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="使用时间",
        help_text="验证码被成功使用后写入时间（一次性）",
    )

    attempts = models.IntegerField(
        default=0,
        verbose_name="尝试次数",
        help_text="用于限制暴力尝试",
    )

    ip = models.CharField(
        max_length=45,
        null=True,
        blank=True,
        verbose_name="请求IP",
        help_text="IPv4/IPv6",
    )

    device_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="设备ID",
        help_text="用于风控识别",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "auth_otp"
        verbose_name = "验证码记录"
        verbose_name_plural = "验证码记录"

        # receiver(191) + purpose(30) 都在索引中，避免索引超长
        indexes = [
            models.Index(fields=["receiver", "purpose"], name="idx_otp_receiver_purpose"),
            models.Index(fields=["created_at"], name="idx_otp_created"),
        ]

    def __str__(self) -> str:
        return f"{self.receiver} - {self.get_purpose_display()}"
```



## 4.5 金币调整页面模板

创建文件：

- `templates/admin/wallet/wallet/adjust.html`

> 注意：确保 `settings.py` 的 `TEMPLATES['DIRS']` 包含 `BASE_DIR / "templates"`（如果你在初始化文档里没加，请补上）。

**adjust.html：**

```html
{% extends "admin/base_site.html" %}
{% load i18n %}

{% block content %}
  <div class="container-fluid">
    <h1>管理员金币调整</h1>

    <div class="card mt-3">
      <div class="card-body">
        <p><strong>用户：</strong>{{ wallet.user }}</p>
        <p><strong>当前余额：</strong>{{ wallet.balance }}</p>
      </div>
    </div>

    <div class="card mt-3">
      <div class="card-body">
        <form method="post" novalidate>
          {% csrf_token %}

          <div class="mb-3">
            <label class="form-label">{{ form.action.label }}</label>
            {{ form.action }}
            {% if form.action.errors %}<div class="text-danger">{{ form.action.errors }}</div>{% endif %}
          </div>

          <div class="mb-3">
            <label class="form-label">{{ form.amount.label }}</label>
            {{ form.amount }}
            <div class="form-text">{{ form.amount.help_text }}</div>
            {% if form.amount.errors %}<div class="text-danger">{{ form.amount.errors }}</div>{% endif %}
          </div>

          <div class="mb-3">
            <label class="form-label">{{ form.remark.label }}</label>
            {{ form.remark }}
            <div class="form-text">{{ form.remark.help_text }}</div>
            {% if form.remark.errors %}<div class="text-danger">{{ form.remark.errors }}</div>{% endif %}
          </div>

          <button type="submit" class="btn btn-primary">确认提交</button>
          <a class="btn btn-secondary" href="{% url 'admin:wallet_wallet_change' wallet.id %}">返回钱包</a>
        </form>
      </div>
    </div>
  </div>
{% endblock %}
```



# 五、订单与授权模块

apps/orders

## 5.1 设计目标

订单模块记录**交易事实**，授权模块记录**最终权限**：

- PurchaseOrder：订单主表
- PurchaseOrderItem：订单项
- PurchaseLicense：授权（权限判断依据）

后台策略：

- **只读**（订单是交易事实，禁止后台改动）



## 5.2 models.py

apps/orders/models.py

```python
from django.db import models
from django.conf import settings
from apps.content.models import Movie


class PurchaseOrder(models.Model):
    """
    购买订单主表
    """

    class Status(models.TextChoices):
        CREATED = "CREATED", "已创建"
        COMPLETED = "COMPLETED", "已完成"
        CANCELLED = "CANCELLED", "已取消"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    total_coin = models.BigIntegerField(
        verbose_name="订单总金币",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="订单状态",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "purchase_order"
        verbose_name = "购买订单"
        verbose_name_plural = "购买订单"

    def __str__(self) -> str:
        return f"订单#{self.id} - {self.user}"
class PurchaseOrderItem(models.Model):
    """
    订单项（对应具体电影）
    """

    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        verbose_name="订单",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    price_coin = models.BigIntegerField(
        verbose_name="购买价格（金豆）",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "purchase_order_item"
        verbose_name = "订单项"
        verbose_name_plural = "订单项"

    def __str__(self) -> str:
        return f"订单#{self.order_id} - {self.movie}"
class PurchaseLicense(models.Model):
    """
    购买授权表
    - 一个用户对一部电影只有一条授权记录
    - 权限判断以此表为准，不以订单为准
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    order_item = models.OneToOneField(
        PurchaseOrderItem,
        on_delete=models.CASCADE,
        verbose_name="订单项",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="授权时间",
    )

    class Meta:
        db_table = "purchase_license"
        verbose_name = "购买授权"
        verbose_name_plural = "购买授权"
        unique_together = ("user", "movie")

    def __str__(self) -> str:
        return f"{self.user} - {self.movie}"
```



## 5.3 forms.py

```python
# apps/orders/forms.py
# 订单与授权均由系统生成，后台不提供编辑表单
```



## 5.4 admin.py

apps/orders/admin.py

```python
from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem, PurchaseLicense


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("movie", "price_coin", "created_at")


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_coin", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "user__email")
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ("user", "total_coin", "status", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PurchaseLicense)
class PurchaseLicenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")
    readonly_fields = ("user", "movie", "order_item", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```



# 六、会员模块

## 6.1 设计目标

会员模块只描述会员有效期，不处理扣费与支付。

后台策略：

- 只读（避免人为延长会员造成对账风险）



## 6.2 models.py

apps/membership/models.py

```python
from django.db import models
from django.conf import settings


class Membership(models.Model):
    """
    用户会员表
    """

    class Plan(models.TextChoices):
        MONTH = "MONTH", "月卡"
        YEAR = "YEAR", "年卡"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "生效中"
        GRACE = "GRACE", "宽限期"
        EXPIRED = "EXPIRED", "已过期"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    plan = models.CharField(
        max_length=20,
        choices=Plan.choices,
        verbose_name="会员类型",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="会员状态",
    )

    start_at = models.DateTimeField(
        verbose_name="开始时间",
    )
    end_at = models.DateTimeField(
        verbose_name="结束时间",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "membership"
        verbose_name = "会员"
        verbose_name_plural = "会员"

    def __str__(self) -> str:
        return f"{self.user} - {self.plan} - {self.status}"
```



## 6.3 forms.py

```python
# apps/membership/forms.py
# 会员状态由系统控制，后台不提供编辑表单
```



## 6.4 admin.py

apps/membership/admin.py

```python
from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "status", "start_at", "end_at")
    list_filter = ("plan", "status")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("user", "plan", "status", "start_at", "end_at", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```



# 七、下载与风控模块

## 7.1 设计目标

下载模块用于审计与风控排查：

- DownloadToken：短期下载凭证
- DownloadDailyQuota：每日次数统计

后台策略：

- 只读（下载令牌与配额由系统生成）



## 7.2 models.py

apps/download/models.py

```python
from django.db import models
from django.conf import settings
from apps.content.models import Movie


class DownloadToken(models.Model):
    """
    下载令牌（短期有效）
    - 由系统生成
    - 用于允许某设备在有效期内下载
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    device_id = models.CharField(
        max_length=64,
        verbose_name="设备ID",
    )
    expires_at = models.DateTimeField(
        verbose_name="过期时间",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "download_token"
        verbose_name = "下载令牌"
        verbose_name_plural = "下载令牌"

    def __str__(self) -> str:
        return f"{self.user} - {self.movie} - {self.device_id}"
class DownloadDailyQuota(models.Model):
    """
    下载每日配额统计
    - 用于限制每日下载次数
    - unique_together 用于并发场景下保证唯一行
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    date = models.DateField(
        verbose_name="日期",
    )
    count = models.IntegerField(
        default=0,
        verbose_name="已使用次数",
    )

    class Meta:
        db_table = "download_daily_quota"
        verbose_name = "下载每日配额"
        verbose_name_plural = "下载每日配额"
        unique_together = ("user", "movie", "date")

    def __str__(self) -> str:
        return f"{self.user} - {self.movie} - {self.date}（{self.count}次）"
```



## 7.3 forms.py

```python
# apps/download/forms.py
# 下载风控数据由系统生成，后台不提供编辑表单
```



## 7.4 admin.py

apps/download/admin.py

```python
from django.contrib import admin
from .models import DownloadToken, DownloadDailyQuota


@admin.register(DownloadToken)
class DownloadTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "device_id", "expires_at", "created_at")
    list_filter = ("expires_at",)
    search_fields = ("user__username", "movie__title", "device_id")
    readonly_fields = ("user", "movie", "device_id", "expires_at", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DownloadDailyQuota)
class DownloadDailyQuotaAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "date", "count")
    list_filter = ("date",)
    search_fields = ("user__username", "movie__title")
    readonly_fields = ("user", "movie", "date", "count")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```



# 八、迁移与执行

因为 CoinTransaction 增加了字段，属于结构变更，这里必须重新迁移。

生成迁移

```bash
python manage.py makemigrations
```

执行迁移

```bash
python manage.py migrate
```

启动服务

```bash
python manage.py runserver
```



后台验证

- 进入：`/admin/`
- 打开“钱包”列表
- 点击某用户钱包的“充值/扣减”入口
- 填写金币数量与原因，提交
- 再到“金币流水”查看是否记录了：操作人、备注、变动数量、变动后余额



# 九、模板目录

如果你项目还没有 `templates/` 目录接入，请在 `config/settings.py` 的 `TEMPLATES` 中确认：

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # 必须包含这行
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

