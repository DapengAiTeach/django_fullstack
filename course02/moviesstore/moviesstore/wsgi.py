"""
WSGI config for moviesstore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置Django的设置模块环境变量
# 这个变量告诉Django使用哪个settings文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesstore.settings')

# 获取WSGI应用对象
# 这个对象会被WSGI服务器（如Gunicorn、uWSGI）调用
application = get_wsgi_application()
