from django.contrib import admin as django_admin


def admin_context(request):
    """
    为 admin 模板提供上下文数据

    提供的变量:
    - site_title: 网站标题
    - site_header: 网站标题（备用）
    - site_brand: 品牌名称
    - welcome_sign: 欢迎信息
    - admin_site: Django admin 网站实例
    """
    return {
        'site_title': 'Movies Store Admin',
        'site_header': 'Movies Store',
        'site_brand': 'Movies Store',
        'welcome_sign': 'Welcome to Movies Store Admin System',
        'admin_site': django_admin.site,
    }
