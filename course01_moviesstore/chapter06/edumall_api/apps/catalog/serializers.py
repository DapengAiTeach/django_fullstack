from rest_framework import serializers
from django.db.models import Avg

from apps.catalog.models import Product
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewReadSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    ModelSerializer：从 Model 自动推导字段
    适用场景：绝大多数 CRUD 资源

    read_only_fields：
    - id/created_at/updated_at 由系统生成，不允许客户端写入
    """

    class Meta:
        model = Product
        fields = ["id", "title", "sku", "price", "stock", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_price(self, value):
        """
        字段级校验：price 必须 >= 0
        """
        if value < 0:
            raise serializers.ValidationError("price 不能为负数")
        return value

    def validate(self, attrs):
        """
        对象级校验：示例规则
        - 如果 is_active=True（上架），要求 stock > 0
        """
        is_active = attrs.get("is_active")
        stock = attrs.get("stock")

        # 部分更新时，attrs 里可能没有 stock/is_active，需要合并 instance 的值
        if self.instance is not None:
            if is_active is None:
                is_active = self.instance.is_active
            if stock is None:
                stock = self.instance.stock

        if is_active and (stock is None or stock <= 0):
            raise serializers.ValidationError({"stock": "上架商品必须保证 stock > 0"})
        return attrs

    def create(self, validated_data):
        """
        覆盖 create：示例增强点
        - 标题去除首尾空格
        - SKU 统一大写
        """
        validated_data["title"] = validated_data["title"].strip()
        validated_data["sku"] = validated_data["sku"].strip().upper()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        覆盖 update：示例增强点
        - SKU 更新时也统一大写
        """
        if "sku" in validated_data:
            validated_data["sku"] = validated_data["sku"].strip().upper()
        if "title" in validated_data:
            validated_data["title"] = validated_data["title"].strip()
        return super().update(instance, validated_data)


class ProductDetailSerializer(ProductSerializer):
    """
    嵌套序列化 + SerializerMethodField（自定义字段）

    详情接口返回：
    - reviews：嵌套评价列表（只读）
    - review_count：评价数量
    - avg_rating：平均评分
    - is_hot：是否热门
    """

    reviews = ReviewReadSerializer(many=True, read_only=True)

    review_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ["reviews", "review_count", "avg_rating", "is_hot"]

    def get_review_count(self, obj: Product) -> int:
        # related_name="reviews" 直接 obj.reviews.count()
        return obj.reviews.count()

    def get_avg_rating(self, obj: Product):
        # 聚合计算：没有评价时返回 None
        return obj.reviews.aggregate(v=Avg("rating"))["v"]

    def get_is_hot(self, obj: Product) -> bool:
        """
        热门规则（示例）：
        - 评价数 >= 2
        - 平均评分 >= 4.5
        """
        count = obj.reviews.count()
        avg = self.get_avg_rating(obj)
        return bool(count >= 2 and avg is not None and float(avg) >= 4.5)