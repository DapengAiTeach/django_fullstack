from django import forms


class AdminCoinAdjustForm(forms.Form):
    """
    管理员金币调整表单（后台入口使用）
    - amount：正整数
    - action：充值 or 扣减
    - remark：原因（必填）
    """

    ACTION_RECHARGE = "RECHARGE"
    ACTION_DEDUCT = "DEDUCT"

    action = forms.ChoiceField(
        label="操作类型",
        choices=(
            (ACTION_RECHARGE, "充值金币（增加）"),
            (ACTION_DEDUCT, "扣减金币（减少）"),
        ),
        required=True,
    )

    amount = forms.IntegerField(
        label="金币数量",
        min_value=1,
        help_text="必须为正整数",
        required=True,
    )

    remark = forms.CharField(
        label="备注（原因）",
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="必须填写操作原因，便于审计追责",
    )