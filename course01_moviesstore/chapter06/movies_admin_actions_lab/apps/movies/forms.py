
from django import forms

class ChangeStatusForm(forms.Form):
    """
    Action 确认页表单
    """
    confirm = forms.BooleanField(label="我确认要执行该批量操作")
    remark = forms.CharField(
        label="操作备注",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )