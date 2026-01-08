# movies/forms.py
from django import forms

SORT_CHOICES = [
    ("-created_at", "最新创建"),
    ("created_at", "最早创建"),
    ("-rating", "评分从高到低"),
    ("rating", "评分从低到高"),
]

class MovieFilterForm(forms.Form):
    kw = forms.CharField(required=False, label="关键词（标题）")
    category = forms.CharField(required=False, label="分类")
    is_active = forms.ChoiceField(
        required=False,
        choices=[("", "全部"), ("1", "上架"), ("0", "下架")],
        label="上架状态",
    )
    sort = forms.ChoiceField(required=False, choices=SORT_CHOICES, initial="-created_at", label="排序")