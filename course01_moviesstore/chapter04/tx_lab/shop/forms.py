# shop/forms.py
from django import forms

class OrderCreateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label="购买数量")

class PayCallbackForm(forms.Form):
    payment_no = forms.CharField(max_length=64, label="支付单号（模拟第三方）")