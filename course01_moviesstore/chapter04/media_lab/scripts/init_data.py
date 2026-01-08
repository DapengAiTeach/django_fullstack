"""
ORM + Media 实验室：初始化数据（可独立运行）
-----------------------------------------
执行：
python scripts/init_data.py

说明：
- 创建电影基础数据（不自动生成图片）
- 图片建议用页面上传，更符合媒体管理教学
"""

import os
import sys
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from movies.models import Movie, MoviePhoto  # MoviePhoto 用于清理
# 不删除 media 文件：让 signals 接管（删记录会删文件）

TITLES = ["星际穿越", "盗梦空间", "黑客帝国", "无间道", "阿甘正传", "教父", "霸王别姬", "流浪地球"]
DESC = [
    "一段关于时间与选择的故事。",
    "当梦境与现实交错，真相不止一层。",
    "经典科幻设定，值得反复回味。",
    "节奏紧凑，反转层层推进。",
]

def main():
    print("🚀 初始化电影数据（不含图片）...")

    # 先清子表再清父表（会触发 signals 自动删文件；但这里无文件也没事）
    MoviePhoto.objects.all().delete()
    Movie.objects.all().delete()

    rows = []
    for i in range(12):
        rows.append(
            Movie(
                title=random.choice(TITLES) + f" · 第{i+1}版",
                description=random.choice(DESC),
            )
        )
    Movie.objects.bulk_create(rows)

    print("✅ 电影：", Movie.objects.count())
    print("✨ 完成！访问 /movies/new/ 上传封面和剧照。")

if __name__ == "__main__":
    main()