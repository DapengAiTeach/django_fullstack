"""
用户应用配置文件

该文件定义了用户应用的配置信息，包括应用名称、显示名称等。
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    用户应用配置类
    
    继承自Django的AppConfig基类，用于配置用户应用的基本信息。
    """
    
    # 应用的Python路径
    # 格式：'应用目录名.应用配置类名'
    default_auto_field = 'django.db.models.BigAutoField'
    
    # 应用名称
    # 用于在Django系统中唯一标识这个应用
    # 必须与INSTALLED_APPS中配置的名称一致
    name = 'apps.users'
    
    # 应用显示名称
    # 用于在Admin后台等地方显示应用名称
    verbose_name = '用户管理'
    
    def ready(self):
        """
        应用就绪时调用
        
        在应用加载完成后注册信号处理器。
        """
        super().ready()
        
        # 导入信号模块
        from . import signals
