from decimal import Decimal
from django import forms
from apps.movies.models import Movie

class BaseMovieAdminForm(forms.ModelForm):
    """
    ✅ 通用基类：控件定制（widget/attrs/help_text）统一放这里
    """
    class Meta:
        model = Movie
        fields = "__all__"
        widgets = {
            # ✅ widget + attrs：让输入更“后台友好”
            "title": forms.TextInput(attrs={"class": "vTextField", "placeholder": "例如：星际远航：序章"}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0", "style": "width: 180px;"}),
            "discount": forms.NumberInput(attrs={"min": "0", "max": "90", "style": "width: 180px;"}),
        }
        help_texts = {
            "title": "建议使用标准片名，便于搜索与运营统计。",
            "price": "必须大于 0。",
            "discount": "0~90，表示折扣百分比，例如 20 表示打 8 折。",
        }

    # ✅ 字段级校验：clean_<field>()
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            return price
        if price <= 0:
            raise forms.ValidationError("原价必须大于 0")
        return price

    def clean_discount(self):
        discount = self.cleaned_data.get("discount")
        if discount is None:
            return discount
        if discount < 0 or discount > 90:
            raise forms.ValidationError("折扣必须在 0~90 之间")
        return discount

    # ✅ 表单级校验：clean()
    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        discount = cleaned.get("discount")

        # 这里演示：折扣过大时给出业务限制（例如不允许低于 1 元）
        if price is not None and discount is not None:
            final_price = price * (Decimal(100) - Decimal(discount)) / Decimal(100)
            if final_price < Decimal("1.00"):
                raise forms.ValidationError("折扣过大导致最终价低于 1 元，请调整折扣或原价。")

        return cleaned


class MovieCreateForm(BaseMovieAdminForm):
    """
    ✅ 新增表单：新增时 title 可编辑（默认即可），风险等级一般不让运营碰
    """
    pass


class MovieChangeForm(BaseMovieAdminForm):
    """
    ✅ 编辑表单：编辑时更严
    - title 变只读：避免被误改（在 admin.py 的 get_readonly_fields 里配合）
    - 也可以在 form 中做 UI 限制：disabled=True（但注意：disabled 不会提交值）
    """
    pass