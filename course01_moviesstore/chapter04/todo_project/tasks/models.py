from django.db import models

class Task(models.Model):
    """
    Task 模型：用来演示 CRUD 的最小可用业务对象
    - title: 标题（CharField）
    - description: 备注（TextField，可空）
    - priority: 优先级（choices + default）
    - is_done: 是否完成（BooleanField）
    - created_at: 创建时间（DateTimeField）
    """

    PRIORITY_CHOICES = [
        (1, "低"),
        (2, "中"),
        (3, "高"),
    ]

    title = models.CharField(max_length=120, verbose_name="标题")

    # blank=True：表单允许为空
    # null=True：数据库允许存 NULL
    description = models.TextField(blank=True, null=True, verbose_name="备注")

    # choices：限定字段取值范围；default：默认值
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="优先级")

    is_done = models.BooleanField(default=False, verbose_name="是否完成")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "任务"
        verbose_name_plural = "任务"

    def __str__(self):
        return self.title