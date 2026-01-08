"""
事务控制实验室：初始化数据（可独立运行）
--------------------------------------
执行：
python scripts/init_data.py
"""

import os
import sys
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from shop.models import Product, Order, OrderItem

def main():
    print("🚀 初始化事务演示数据...")

    # 清理：先子表再父表
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()

    Product.objects.bulk_create([
        Product(name="电影票·IMAX", price=Decimal("68.00"), stock=5),
        Product(name="电影票·普通厅", price=Decimal("39.00"), stock=10),
        Product(name="会员卡·月卡", price=Decimal("25.00"), stock=3),
        Product(name="周边·海报", price=Decimal("19.90"), stock=8),
        Product(name="并发演示专用（库存=1）", price=Decimal("9.90"), stock=1),
    ])

    print("✅ 商品：", Product.objects.count())
    print("✨ 完成！访问 /products/ 开始下单与事务演示。")

if __name__ == "__main__":
    main()