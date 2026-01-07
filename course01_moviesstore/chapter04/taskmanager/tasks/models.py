from django.db import models


class Task(models.Model):
    # 任务标题
    title = models.CharField(max_length=200, verbose_name="任务标题")

    # 任务描述
    description = models.TextField(blank=True, null=True, verbose_name="任务描述")

    # 任务优先级
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    PRIORITY_CHOICES = [
        (HIGH, '高'),
        (MEDIUM, '中'),
        (LOW, '低'),
    ]
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
        verbose_name="优先级"
    )

    # 任务状态
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (NOT_STARTED, '未开始'),
        (IN_PROGRESS, '进行中'),
        (COMPLETED, '已完成'),
    ]
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=NOT_STARTED,
        verbose_name="任务状态"
    )

    # 任务创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 任务最后更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    def __str__(self):
        return self.title
