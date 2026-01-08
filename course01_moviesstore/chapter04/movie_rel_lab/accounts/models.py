from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    OneToOneField：用户扩展模型（必会）
    - 一个用户对应一份扩展资料
    - 常用于：头像、手机号、地址、会员等级等
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 用户删除 => 资料一起删除（最常见）
        related_name="profile",
    )
    nickname = models.CharField("昵称", max_length=30, blank=True)
    vip_level = models.PositiveSmallIntegerField("VIP等级", default=0)

    def __str__(self):
        return self.nickname or self.user.username
