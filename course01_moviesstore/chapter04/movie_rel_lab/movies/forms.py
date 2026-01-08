# movies/forms.py
from django import forms
from .models import Movie

class OrderCreateForm(forms.Form):
    """
    用普通 Form 更适合教学：
    - movie_ids 多选
    - quantities 用简单输入（演示中间表写入逻辑）
    """
    movie_ids = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="选择电影",
    )
    quantity = forms.IntegerField(min_value=1, initial=1, label="每部数量（统一）")