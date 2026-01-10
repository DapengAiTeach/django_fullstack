from django.contrib import admin

def apply_admin_branding(site: admin.AdminSite, *, header: str, title: str, index_title: str) -> None:
    """
    Admin 品牌化：企业后台常规配置
    """
    site.site_header = header
    site.site_title = title
    site.index_title = index_title