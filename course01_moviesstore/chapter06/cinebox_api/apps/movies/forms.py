from django import forms
from apps.movies.models import Movie


class MovieForm(forms.ModelForm):
    """
    Django Form（传统服务端表单）：
    - 主要用于服务端渲染 HTML 表单/管理后台增强
    - 与 DRF Serializer 不同：Serializer 更面向 API 的 JSON 输入输出
    """

    class Meta:
        model = Movie
        fields = ["title", "overview", "release_date", "rating"]