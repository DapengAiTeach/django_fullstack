"""
用户应用Admin后台配置文件

该文件定义了用户模型在Admin后台的显示和管理方式。
"""

from django.contrib import admin

# 暂时不注册任何模型到Admin后台
# 避免循环导入问题
# 可以在用户创建后通过信号自动创建UserProfile
