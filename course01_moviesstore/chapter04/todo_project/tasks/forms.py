from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    ModelForm：把模型字段直接映射为表单字段
    页面上提交 -> 表单校验 -> 保存到数据库
    """

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "is_done"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "例如：学习 Django ORM CRUD",
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "可选：补充备注",
                },
            ),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "is_done": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
