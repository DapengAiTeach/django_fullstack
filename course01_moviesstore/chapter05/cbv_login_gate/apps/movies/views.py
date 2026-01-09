from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = "movies/home.html"

class VipCBVView(LoginRequiredMixin, TemplateView):
    """
    ✅ 正确写法：LoginRequiredMixin 必须放最左边！

    工作原理（必须讲清）：
    - LoginRequiredMixin 重写了 dispatch()
    - dispatch() 是 CBV 的总入口（get/post 都从这里进）
    - 未登录时，dispatch() 直接返回重定向到 LOGIN_URL，并拼接 next

    关键点：
    - 只要 MRO 让 LoginRequiredMixin.dispatch 先被找到，门禁就生效。
    """
    template_name = "movies/vip_cbv.html"

class MROExplainView(TemplateView):
    """
    用页面把 MRO（方法解析顺序）展示出来，让学生一眼看到“为什么要放最左边”。
    """
    template_name = "movies/mro.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vip_mro"] = [c.__name__ for c in VipCBVView.mro()]
        return ctx

class DebugView(TemplateView):
    """
    调试页：显示登录状态、当前 user、并提示常见错误排查点。
    """
    template_name = "movies/debug.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["is_auth"] = user.is_authenticated
        ctx["username"] = getattr(user, "username", "")
        ctx["login_url_setting"] = "accounts:login"
        return ctx