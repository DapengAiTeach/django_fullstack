# movies/forms.py
from django import forms


class ReviewCreateForm(forms.Form):
    nickname = forms.CharField(max_length=30, label="昵称")
    score = forms.IntegerField(min_value=1, max_value=10, initial=8, label="评分(1-10)")
    content = forms.CharField(max_length=200, label="评论内容", widget=forms.Textarea(attrs={"rows": 3}))
