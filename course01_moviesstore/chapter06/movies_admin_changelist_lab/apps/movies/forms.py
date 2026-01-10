from django import forms
from apps.movies.models import Movie

class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
        widgets = {
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0", "style": "width:160px;"}),
            "score": forms.NumberInput(attrs={"step": "0.1", "min": "0", "max": "10", "style": "width:160px;"}),
            "poster_url": forms.URLInput(attrs={"placeholder": "https://...jpg", "style": "width: 520px;"}),
        }
        help_texts = {
            "title": "支持业务搜索：例如 `g:科幻 d:诺兰 片名关键词`（在列表页搜索框输入）。",
            "poster_url": "建议使用稳定的图片 URL（为空则不显示预览）。",
        }