from decimal import Decimal
from django import forms
from django.forms.models import BaseInlineFormSet

from apps.movies.models import OrderItem, Movie

class OrderItemInlineForm(forms.ModelForm):
    """
    Inline 单行表单：演示 clean_<field>() + clean()
    """
    class Meta:
        model = OrderItem
        fields = ["movie", "quantity", "unit_price"]

        widgets = {
            "quantity": forms.NumberInput(attrs={"min": "1", "style": "width:120px;"}),
            "unit_price": forms.NumberInput(attrs={"step": "0.01", "min": "0", "style": "width:140px;"}),
        }
        help_texts = {
            "movie": "选择要下单的电影商品。",
            "quantity": "数量必须 >= 1。",
            "unit_price": "成交单价可调整，但不能为 0。",
        }

    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity")
        if qty is None or qty < 1:
            raise forms.ValidationError("数量必须 >= 1")
        return qty

    def clean_unit_price(self):
        price = self.cleaned_data.get("unit_price")
        if price is None or price <= 0:
            raise forms.ValidationError("成交单价必须 > 0")
        return price

    def clean(self):
        cleaned = super().clean()
        movie: Movie = cleaned.get("movie")
        unit_price = cleaned.get("unit_price")

        # 演示：成交价不允许低于商品售价的 50%（防误操作）
        if movie and unit_price is not None:
            if unit_price < (movie.price * Decimal("0.5")):
                raise forms.ValidationError("成交单价过低（低于商品售价的 50%），请确认后修改。")
        return cleaned


class OrderItemInlineFormSet(BaseInlineFormSet):
    """
    Inline 表单集校验：一次性校验多行（非常关键）
    """
    def clean(self):
        super().clean()

        movies_seen = set()
        valid_count = 0
        total_qty = 0

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            # 被标记删除的行不参与校验
            if form.cleaned_data.get("DELETE"):
                continue

            movie = form.cleaned_data.get("movie")
            qty = form.cleaned_data.get("quantity")

            # 空行（例如 extra 生成的空白行）跳过
            if not movie and not qty:
                continue

            valid_count += 1

            if movie:
                if movie.pk in movies_seen:
                    raise forms.ValidationError("同一订单中不能重复选择同一部电影（请合并数量）。")
                movies_seen.add(movie.pk)

            if qty:
                total_qty += int(qty)

        if valid_count < 1:
            raise forms.ValidationError("订单至少需要 1 条明细。")

        # 演示：限制总数量（配合 max_num 的“UI限制”，这里做“后端强制”）
        if total_qty > 10:
            raise forms.ValidationError("订单总数量不能超过 10（演示规则）。")