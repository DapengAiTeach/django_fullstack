from django import forms
from apps.movies.models import Movie

class MovieAdminForm(forms.ModelForm):
    """
    Admin 专用表单：演示“业务校验 + 表单增强”
    """
    class Meta:
        model = Movie
        fields = "__all__"

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is not None and stock < 0:
            raise forms.ValidationError("库存不能为负数")
        return stock