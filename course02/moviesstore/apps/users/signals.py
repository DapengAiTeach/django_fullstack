"""
用户应用信号文件

该文件定义了用户应用的信号处理，用于在用户创建时自动初始化用户数据。
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# 获取自定义的User模型
User = get_user_model()


@receiver(post_save, sender=User)
def initialize_user_data(sender, instance, created, **kwargs):
    """
    初始化用户数据
    
    当用户创建时，自动初始化用户的金币余额和会员等级。
    这些字段已经在User模型中定义，并设置了默认值，
    所以这里不需要做任何操作，保留此函数作为示例。
    
    Args:
        sender: 信号发送者（User模型）
        instance: 用户实例
        created: 是否为新创建的用户
        **kwargs: 其他参数
    """
    # User模型中的coins和member_level字段已经有默认值
    # coins默认为0，member_level默认为'normal'
    # 所以这里不需要做任何操作
    pass
