"""
Django项目配置文件

该文件包含了电影商城项目的所有配置项，包括数据库、静态文件、媒体文件、中间件等设置。
"""

import os
from pathlib import Path

# 项目根目录
# 通过__file__获取当前文件的路径，然后向上两级得到项目根目录
# BASE_DIR用于构建其他相对路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥
# 用于加密签名，确保数据安全
# 生产环境必须修改为一个随机生成的密钥，可以使用：python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# 调试模式
# True表示开发模式，会显示详细的错误信息
# False表示生产模式，只显示简化的错误信息
# 生产环境必须设置为False
DEBUG = True

# 允许的主机
# 允许访问该Django应用的主机名或IP地址列表
# '*'表示允许所有主机，仅用于开发环境
# 生产环境应该设置为具体的域名，如：['example.com', 'www.example.com']
ALLOWED_HOSTS = ['*']

# 已安装的应用
# Django会按照列表顺序加载这些应用
# django.contrib.* 是Django内置的应用
INSTALLED_APPS = [
    'django.contrib.admin',           # Django管理后台
    'django.contrib.auth',            # 认证系统（用户、权限、组）
    'django.contrib.contenttypes',     # 内容类型框架（用于模型权限）
    'django.contrib.sessions',         # 会话框架
    'django.contrib.messages',         # 消息框架（用于显示提示信息）
    'django.contrib.staticfiles',      # 静态文件管理
    # 自定义应用：
    'apps.users.apps.UsersConfig',    # 用户应用
    # 'apps.movies',                 # 电影应用
    # 'apps.orders',                 # 订单应用
    # 'apps.coins',                  # 金币应用
    # 'apps.reviews',                # 评价评论应用
    # 'apps.favorites',              # 收藏应用
]

# 中间件
# 中间件是处理请求和响应的钩子，按列表顺序执行
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # 安全中间件，提供安全相关的HTTP头
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话中间件，管理用户会话
    'django.middleware.common.CommonMiddleware',            # 通用中间件，处理URL规范化等
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF保护中间件，防止跨站请求伪造
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 认证中间件，将用户信息添加到请求中
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件，处理临时消息
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 点击劫持保护中间件
]

# 根URL配置
# 指定主路由文件的Python路径
ROOT_URLCONF = 'moviesstore.urls'

# 模板配置
# 定义Django如何查找和渲染模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 模板引擎后端
        'DIRS': [BASE_DIR / 'templates'],  # 模板目录列表，Django会按顺序查找
        'APP_DIRS': True,  # 是否在每个应用的templates目录中查找模板
        'OPTIONS': {
            'context_processors': [
                # 上下文处理器，将变量注入到所有模板中
                'django.template.context_processors.debug',      # DEBUG变量
                'django.template.context_processors.request',     # request变量
                'django.contrib.auth.context_processors.auth',   # user变量（当前登录用户）
                'django.contrib.messages.context_processors.messages', # messages变量（临时消息）
            ],
        },
    },
]

# WSGI应用
# 指定WSGI应用的Python路径，用于部署
WSGI_APPLICATION = 'moviesstore.wsgi.application'

# 数据库配置
# 定义数据库连接信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # 数据库引擎，使用SQLite3
        'NAME': BASE_DIR / 'db.sqlite3',       # 数据库文件路径
        # 如果要使用MySQL或PostgreSQL，配置如下：
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'moviesstore',
        # 'USER': 'root',
        # 'PASSWORD': 'password',
        # 'HOST': 'localhost',
        # 'PORT': '3306',
    }
}

# 密码验证器
# 用于验证用户密码的强度
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # 检查密码是否与用户信息过于相似
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # 检查密码最小长度
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # 检查密码是否为常见密码
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # 检查密码是否全为数字
    },
]

# 语言代码
# 设置网站使用的语言
# 'zh-hans' 表示简体中文
LANGUAGE_CODE = 'zh-hans'

# 时区
# 设置网站使用的时区
# 'Asia/Shanghai' 表示中国上海时区（UTC+8）
TIME_ZONE = 'Asia/Shanghai'

# 是否启用国际化
# True表示支持多语言
USE_I18N = True

# 是否启用时区支持
# True表示使用时区感知的datetime对象
USE_TZ = True

# 静态文件URL
# 静态文件（CSS、JS、图片等）的URL前缀
STATIC_URL = 'static/'

# 静态文件目录
# 额外的静态文件目录列表，Django会在这里查找静态文件
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 静态文件收集目录
# 运行collectstatic命令时，静态文件会被收集到这个目录
# 生产环境使用STATIC_ROOT，开发环境使用STATICFILES_DIRS
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 媒体文件URL
# 用户上传的文件（头像、电影封面、视频等）的URL前缀
MEDIA_URL = 'media/'

# 媒体文件目录
# 用户上传的文件存储的目录
MEDIA_ROOT = BASE_DIR / 'media'

# 默认自增字段类型
# 指定模型中AutoField的默认类型
# BigAutoField使用64位整数，支持更大的ID范围
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 自定义用户模型
# 指定使用自定义的User模型，而不是Django默认的User模型
# 格式：'app_label.ModelName'
AUTH_USER_MODEL = 'users.User'

# 登录URL
# 用户需要登录时重定向到的URL
# 使用命名空间格式：'应用名:url名称'
LOGIN_URL = 'users:login'

# 登录成功后重定向URL
# 用户登录成功后重定向到的URL
LOGIN_REDIRECT_URL = 'index'

# 登出后重定向URL
# 用户登出后重定向到的URL
LOGOUT_REDIRECT_URL = 'index'
