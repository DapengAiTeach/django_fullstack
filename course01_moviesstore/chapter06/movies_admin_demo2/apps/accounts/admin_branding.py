from django.contrib import admin


def apply_admin_branding(site: admin.AdminSite, *, header: str, title: str, index_title: str) -> None:
    """
    对 AdminSite 做品牌化（site_header / site_title / index_title）
    """
    site.site_header = header
    site.site_title = title
    site.index_title = index_title
