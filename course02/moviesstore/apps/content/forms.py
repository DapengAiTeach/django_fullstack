from django import forms
from .models import Movie


class MovieAdminForm(forms.ModelForm):
    """
    后台电影表单
    """

    class Meta:
        model = Movie
        fields = "__all__"

    def clean_price_coin(self):
        price = self.cleaned_data["price_coin"]
        if price < 0:
            raise forms.ValidationError("价格不能为负数")
        return price