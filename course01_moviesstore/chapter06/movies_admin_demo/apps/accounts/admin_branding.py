from django.contrib import admin


def apply_admin_branding(
        site: admin.AdminSite,
        *,
        header: str,
        title: str,
        index_title: str,
) -> None:
    """
    给 AdminSite 做品牌化
    你可以对默认 admin.site 或 自定义 AdminSite 都调用它。
    """
    site.site_header = header
    site.site_title = title
    site.index_title = index_title
