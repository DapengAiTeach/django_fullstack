"""
电影数据初始化脚本
---------------------------------
用途：
- 为“列表页 / 排序 / 聚合 / 分页”课程准备测试数据
- 可反复执行（会先清空 Movie 表）
- 适合教学 & 演示

执行方式：
python scripts/init_movies.py
"""

import os
import sys
import random
from decimal import Decimal
from datetime import timedelta

# =========================
# 1️⃣ 初始化 Django 环境
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

# =========================
# 2️⃣ 导入模型
# =========================

from django.utils import timezone
from movies.models import Movie, CATEGORY_CHOICES

# =========================
# 3️⃣ 配置造数参数
# =========================

TOTAL_MOVIES = 60   # 生成多少条数据

TITLES = [
    "星际穿越", "黑客帝国", "盗梦空间", "银翼杀手",
    "这个杀手不太冷", "霸王别姬", "泰坦尼克号",
    "教父", "阿甘正传", "低俗小说", "蝙蝠侠",
    "复仇者联盟", "流浪地球", "速度与激情",
    "疯狂的石头", "无间道", "唐人街探案",
]

# =========================
# 4️⃣ 清空旧数据（教学非常重要）
# =========================

print("🚀 开始初始化电影数据...")
Movie.objects.all().delete()
print("✅ 已清空 Movie 表")

# =========================
# 5️⃣ 批量创建数据
# =========================

movies = []

for i in range(TOTAL_MOVIES):
    title = random.choice(TITLES) + f" · 第{i+1}版"

    category, _ = random.choice(CATEGORY_CHOICES)

    rating = round(random.uniform(5.0, 9.8), 1)
    price = Decimal(random.randint(30, 120))
    stock = random.randint(0, 500)

    is_hot = random.random() < 0.3  # 约 30% 是热门

    created_at = timezone.now() - timedelta(days=random.randint(0, 90))

    movies.append(
        Movie(
            title=title,
            category=category,
            rating=rating,
            price=price,
            stock=stock,
            is_hot=is_hot,
            created_at=created_at,
        )
    )

Movie.objects.bulk_create(movies)

# =========================
# 6️⃣ 输出结果
# =========================

print(f"🎬 成功生成 {TOTAL_MOVIES} 条电影数据")
print("📊 可直接用于：")
print("   - order_by() 排序演示")
print("   - aggregate() 聚合统计")
print("   - annotate() 分组统计")
print("   - Paginator 分页联动")
print("✨ 数据初始化完成！")