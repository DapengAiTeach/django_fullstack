from django import template

register = template.Library()


@register.simple_tag
def admin_query(cl, key, value):
    """
    在 Django admin 列表页中生成带参数的查询字符串。

    参数：
    - cl: ChangeList 实例（admin 列表页上下文对象）
    - key: 需要更新的参数名（如 "p"）
    - value: 参数值（如 0 表示第一页）

    作用：
    - 保留当前筛选/搜索条件
    - 仅更新指定参数（例如分页参数）
    """
    return cl.get_query_string({key: value})
