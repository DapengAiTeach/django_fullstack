from django.contrib.admin import AdminSite


class OpsAdminSite(AdminSite):
    """
    运营后台
    - 你可以在这里控制：站点标题、站点可见模型、全局 CSS/JS、首页等
    """
    site_header = "运营后台 · Movies Admin Demo"
    site_title = "运营后台"
    index_title = "内容与商品运营"


ops_site = OpsAdminSite(name="ops_admin")
