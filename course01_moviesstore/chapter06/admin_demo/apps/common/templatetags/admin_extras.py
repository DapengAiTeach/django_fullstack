from django import template
from django.contrib import admin as django_admin
from django.apps import apps

register = template.Library()

# Icon mapping for models and apps
ADMIN_ICONS = {
    'auth': 'fas fa-users',
    'auth.user': 'fas fa-user',
    'auth.group': 'fas fa-users-cog',
    'movies': 'fas fa-film',
    'movies.movie': 'fas fa-film',
    'movies.genre': 'fas fa-tags',
    'movies.country': 'fas fa-flag',
    'movies.language': 'fas fa-language',
    'movies.person': 'fas fa-user',
    'movies.moviecredit': 'fas fa-users',
    'home': 'fas fa-home',
    'accounts': 'fas fa-user-shield',
    'common': 'fas fa-cog',
}


@register.simple_tag
def get_admin_icon(model_name):
    """
    获取模型对应的 FontAwesome 图标类名

    用法:
    {% get_admin_icon "movies.Movie" as icon %}
    <i class="{{ icon }}"></i>
    """
    if not model_name:
        return 'fas fa-cube'

    model_name_lower = model_name.lower().replace(' ', '')
    return ADMIN_ICONS.get(model_name_lower, 'fas fa-cube')


@register.simple_tag
def get_app_list():
    """
    获取所有已注册的 admin 应用列表

    返回格式:
    [
        {
            'name': 'Authentication',
            'app_label': 'auth',
            'models': [
                {
                    'name': 'User',
                    'admin_url': '/admin/auth/user/',
                    'icon': 'fas fa-user',
                }
            ]
        }
    ]
    """
    app_list = []
    app_list_dict = {}

    try:
        for model, admin_instance in django_admin.site._registry.items():
            app_label = model._meta.app_label

            # 找到或创建应用条目
            if app_label not in app_list_dict:
                try:
                    app_config = apps.get_app_config(app_label)
                    app_entry = {
                        'name': app_config.verbose_name,
                        'app_label': app_label,
                        'models': []
                    }
                    app_list_dict[app_label] = app_entry
                    app_list.append(app_entry)
                except (LookupError, RuntimeError):
                    # App not found or not ready
                    continue

            app_entry = app_list_dict[app_label]

            # 添加模型
            model_key = f"{app_label}.{model.__name__}".lower()
            model_entry = {
                'name': model._meta.verbose_name_plural,
                'admin_url': f"/admin/{app_label}/{model._meta.model_name}/",
                'icon': ADMIN_ICONS.get(model_key, 'fas fa-cube'),
            }
            app_entry['models'].append(model_entry)

    except Exception:
        # Return empty list if there's any error
        pass

    return app_list


@register.filter
def admin_action_flag(flag_value):
    """
    将 Django admin 日志的操作标志转换为中文

    用法:
    {{ entry.action_flag|admin_action_flag }}
    """
    flags = {
        1: '添加',
        2: '修改',
        3: '删除',
    }
    return flags.get(flag_value, '未知')


@register.filter
def get_admin_link(model):
    """
    获取模型的 admin 变更列表链接

    用法:
    <a href="{{ model|get_admin_link }}">{{ model }}</a>
    """
    if not model:
        return '#'
    return f"/admin/{model._meta.app_label}/{model._meta.model_name}/"


@register.simple_tag
def admin_actions(cl):
    """
    渲染批量操作下拉菜单

    用法:
    {% admin_actions cl %}
    """
    if not hasattr(cl, 'opts') or not cl.opts:
        return ''

    actions = cl.get_actions(None)
    if not actions:
        return ''

    html = '<div class="admin-actions mb-3"><select class="form-select" name="action">'
    html += '<option value="">--- 选择操作 ---</option>'

    for action, action_func in actions:
        html += f'<option value="{action}">{action_func.__doc__ or action}</option>'

    html += '</select><button type="submit" class="btn btn-sm btn-primary ms-2">执行</button></div>'

    return html
