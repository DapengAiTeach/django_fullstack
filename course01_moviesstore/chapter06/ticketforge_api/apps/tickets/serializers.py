from rest_framework import serializers
from apps.tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    校验覆盖：
    - 字段级校验：validate_title / validate_priority
    - 对象级校验：validate
    - raise ValidationError
    """

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "priority", "status", "assignee_email", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value: str):
        value = value.strip()
        if len(value) < 5 or len(value) > 80:
            raise serializers.ValidationError("title 长度必须在 5~80")
        return value

    def validate_priority(self, value: int):
        if value < 1 or value > 5:
            raise serializers.ValidationError("priority 必须在 1~5")
        return value

    def validate(self, attrs):
        """
        对象级校验：
        - status=CLOSED 时必须有 assignee_email
        - status=DONE/CLOSED 不允许 priority=5（示例）
        """
        instance = getattr(self, "instance", None)

        # merge：支持 PATCH 场景（attrs 可能不包含所有字段）
        status = attrs.get("status", instance.status if instance else Ticket.Status.OPEN)
        priority = attrs.get("priority", instance.priority if instance else 3)
        assignee_email = attrs.get("assignee_email", instance.assignee_email if instance else None)

        if status == Ticket.Status.CLOSED and not assignee_email:
            raise serializers.ValidationError({"assignee_email": "status=CLOSED 时必须填写 assignee_email"})

        if status in (Ticket.Status.DONE, Ticket.Status.CLOSED) and priority == 5:
            raise serializers.ValidationError({"priority": "status 为 DONE/CLOSED 时不允许 priority=5"})

        return attrs