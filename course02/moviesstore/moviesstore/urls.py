"""
Django项目主路由配置文件

该文件定义了项目的URL路由规则，将URL映射到对应的视图函数或视图类。
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL模式列表
# Django会按照列表顺序匹配URL，找到第一个匹配的就会停止
urlpatterns = [
    # Django管理后台路由
    # 访问 /admin/ 会进入Django内置的管理后台
    path('admin/', admin.site.urls),

    # Django内置认证路由
    # 包含登录、登出、密码重置等URL
    # 默认模板位置：registration/login.html, registration/logout.html等
    # 可通过settings.py中的LOGIN_URL、LOGOUT_REDIRECT_URL等配置自定义
    path('', include('django.contrib.auth.urls')),

    # 后续会添加自定义应用的路由：
    # path('users/', include('apps.users.urls', namespace='users')),      # 用户应用路由
    # path('movies/', include('apps.movies.urls', namespace='movies')),    # 电影应用路由
    # path('orders/', include('apps.orders.urls', namespace='orders')),    # 订单应用路由
    # path('coins/', include('apps.coins.urls', namespace='coins')),      # 金币应用路由
    # path('reviews/', include('apps.reviews.urls', namespace='reviews')),  # 评价评论应用路由
    # path('favorites/', include('apps.favorites.urls', namespace='favorites')), # 收藏应用路由
]

# 开发环境下的静态文件和媒体文件服务
# 在DEBUG模式下，Django会自动提供静态文件和媒体文件服务
# 在生产环境中，应该使用Nginx等Web服务器来处理这些文件
if settings.DEBUG:
    # 媒体文件URL配置
    # 将MEDIA_URL（如/media/）映射到MEDIA_ROOT目录
    # 用于提供用户上传的文件（头像、电影封面、视频等）
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # 静态文件URL配置
    # 将STATIC_URL（如/static/）映射到STATIC_ROOT目录
    # 用于提供静态文件（CSS、JS、图片等）
    # 注意：开发环境使用STATICFILES_DIRS，生产环境使用STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
