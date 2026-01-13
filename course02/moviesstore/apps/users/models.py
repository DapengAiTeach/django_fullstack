"""
用户模型文件

该文件定义了用户相关的数据模型，包括扩展User模型。
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户模型
    
    继承自Django的AbstractUser，扩展了默认的用户模型。
    添加了手机号、头像、金币余额、会员等级等额外字段。
    """
    
    # 手机号
    # 用于用户登录和找回密码
    phone = models.CharField(
        max_length=11,
        verbose_name='手机号',
        blank=True,
        null=True,
        help_text='请输入11位手机号码'
    )
    
    # 头像
    # 用户上传的个人头像图片
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        verbose_name='头像',
        blank=True,
        null=True,
        default='avatars/default.png',
        help_text='请上传个人头像'
    )
    
    # 生日
    # 用户的出生日期
    birthday = models.DateField(
        verbose_name='生日',
        blank=True,
        null=True,
        help_text='请选择您的生日'
    )
    
    # 性别
    # 用户的性别选择
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密'),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='secret',
        verbose_name='性别',
        help_text='请选择您的性别'
    )
    
    # 个人简介
    # 用户的个人介绍
    bio = models.TextField(
        max_length=500,
        verbose_name='个人简介',
        blank=True,
        null=True,
        help_text='请输入个人简介（最多500字）'
    )
    
    # 金币余额
    # 用户账户中的金币数量
    coins = models.IntegerField(
        default=0,
        verbose_name='金币余额',
        help_text='用户账户中的金币数量'
    )
    
    # 会员等级
    # 用户的会员等级
    MEMBER_LEVEL_CHOICES = (
        ('normal', '普通会员'),
        ('vip', 'VIP会员'),
        ('svip', 'SVIP会员'),
    )
    member_level = models.CharField(
        max_length=10,
        choices=MEMBER_LEVEL_CHOICES,
        default='normal',
        verbose_name='会员等级',
        help_text='用户的会员等级'
    )
    
    # 会员到期时间
    # VIP会员的到期时间
    member_expire_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='会员到期时间',
        help_text='VIP会员的到期时间'
    )
    
    # 创建时间
    # 用户账号创建的时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    # 更新时间
    # 用户信息最后更新的时间
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        """
        模型元数据配置
        """
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']  # 按创建时间倒序排列
    
    def __str__(self):
        """
        字符串表示
        
        返回用户的用户名，用于在Admin后台等地方显示。
        """
        return self.username
    
    def is_vip(self):
        """
        判断是否为VIP会员
        
        Returns:
            bool: 如果是VIP会员且未过期返回True，否则返回False
        """
        from django.utils import timezone
        if self.member_level in ['vip', 'svip']:
            if self.member_expire_at and self.member_expire_at > timezone.now():
                return True
        return False
