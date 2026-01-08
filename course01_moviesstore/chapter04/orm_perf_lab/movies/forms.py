# movies/forms.py
from django import forms

MODE_CHOICES = [
    ("slow", "慢模式（故意N+1）"),
    ("fast", "快模式（select/prefetch）"),
    ("split", "拆分模式（列表轻量化）"),
]

class FeedModeForm(forms.Form):
    mode = forms.ChoiceField(
        choices=MODE_CHOICES,
        initial="fast",
        required=False,
        label="性能模式",
    )