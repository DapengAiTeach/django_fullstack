from django.db import models


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"
        CLOSED = "CLOSED", "Closed"

    title = models.CharField("标题", max_length=80)
    description = models.TextField("描述", blank=True)
    priority = models.PositiveSmallIntegerField("优先级(1~5)", default=3)
    status = models.CharField("状态", max_length=20, choices=Status.choices, default=Status.OPEN)
    assignee_email = models.EmailField("指派邮箱", blank=True, null=True)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "tickets_ticket"
        verbose_name = "工单"
        verbose_name_plural = "工单"

    def __str__(self) -> str:
        return f"{self.title}({self.status})"