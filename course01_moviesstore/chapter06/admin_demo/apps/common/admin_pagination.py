from django.contrib import admin

# 说明：
# Django Admin 默认每页数量是固定值（ModelAdmin.list_per_page）。
# 这里通过重写 ModelAdmin.get_list_per_page，让后台支持 ?per_page= 动态切换。
# 采用“全局猴子补丁”的方式，保证对所有模型列表页统一生效。


def _get_list_per_page(self, request):
    # 读取 ModelAdmin 默认分页值（如未设置则使用 100）
    default_per_page = getattr(self, "list_per_page", 100)

    # 读取用户在 URL 中传入的 per_page 参数
    raw_value = request.GET.get("per_page")
    if not raw_value:
        # 未传参则直接使用默认值
        return default_per_page

    try:
        # 尝试把参数转成整数
        per_page = int(raw_value)
    except ValueError:
        # 非法参数直接回退到默认值，避免报错
        return default_per_page

    # 限制分页大小区间，避免过大值导致性能问题
    if 1 <= per_page <= 500:
        return per_page

    # 超出范围同样回退到默认值
    return default_per_page


# 将方法挂到全局 ModelAdmin 上，所有 admin 列表页均可使用 per_page 参数
admin.ModelAdmin.get_list_per_page = _get_list_per_page
