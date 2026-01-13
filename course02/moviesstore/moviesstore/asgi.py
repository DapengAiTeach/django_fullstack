"""
ASGI config for moviesstore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# 设置Django的设置模块环境变量
# 这个变量告诉Django使用哪个settings文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesstore.settings')

# 获取ASGI应用对象
# 这个对象会被ASGI服务器（如Daphne、Uvicorn）调用
# ASGI支持异步处理，适合WebSocket等实时功能
application = get_asgi_application()
