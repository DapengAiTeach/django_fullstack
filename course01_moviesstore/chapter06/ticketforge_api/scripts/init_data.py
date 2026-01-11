"""
初始化示例数据

执行要求：
- 必须在项目根目录执行：python scripts/init_data.py
- 内置 sys.path.insert 与 DJANGO_SETTINGS_MODULE，避免找不到 config

数据策略：
- 使用 title 作为幂等键（示例），确保脚本可重复执行不污染数据库
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

from apps.tickets.models import Ticket  # noqa: E402


def main():
    seed = [
        {"title": "登录失败排查", "description": "用户反馈无法登录，需排查认证链路。", "priority": 4, "status": Ticket.Status.OPEN},
        {"title": "订单接口超时", "description": "支付回调偶发超时，需定位慢查询。", "priority": 5, "status": Ticket.Status.IN_PROGRESS},
        {"title": "修复前端白屏", "description": "React 构建产物加载失败，检查静态资源路径。", "priority": 3, "status": Ticket.Status.DONE},
        {"title": "发布后回滚", "description": "线上异常，回滚到上一版本并复盘。", "priority": 2, "status": Ticket.Status.CLOSED, "assignee_email": "ops@example.com"},
    ]

    created = 0
    for item in seed:
        obj, is_created = Ticket.objects.get_or_create(
            title=item["title"],
            defaults=item,
        )
        created += 1 if is_created else 0

    print(f"[init_data] created={created}, total={Ticket.objects.count()}")


if __name__ == "__main__":
    main()