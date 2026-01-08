# movies/forms.py
from django import forms
from .models import CATEGORY_CHOICES

SORT_CHOICES = [
    ("-created_at", "最新创建"),
    ("created_at", "最早创建"),
    ("-rating", "评分从高到低"),
    ("rating", "评分从低到高"),
    ("-price", "价格从高到低"),
    ("price", "价格从低到高"),
]

PAGE_SIZE_CHOICES = [
    (5, "5条/页"),
    (10, "10条/页"),
    (20, "20条/页"),
]


class MovieAdminFilterForm(forms.Form):
    """
    ✅ GET 查询表单：
    - clean 后得到“稳定、可信”的字段，用来组装 ORM
    """
    kw = forms.CharField(required=False, label="关键词")
    category = forms.ChoiceField(
        required=False,
        choices=[("", "全部分类")] + CATEGORY_CHOICES,
        label="分类",
    )
    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        initial="-created_at",
        label="排序",
    )
    page_size = forms.ChoiceField(
        required=False,
        choices=PAGE_SIZE_CHOICES,
        initial=10,
        label="每页条数",
    )
