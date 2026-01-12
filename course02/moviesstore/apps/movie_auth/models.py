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
