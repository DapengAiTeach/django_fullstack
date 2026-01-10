from django.contrib import admin

def apply_admin_branding(site: admin.AdminSite, *, header: str, title: str, index_title: str) -> None:
    """
    对 Django AdminSite 做统一品牌化配置：
    - site_header：左上角大标题
    - site_title：浏览器 tab 标题
    - index_title：首页欢迎标题
    """
    site.site_header = header
    site.site_title = title
    site.index_title = index_title
