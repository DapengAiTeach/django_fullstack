from rest_framework import serializers
from apps.reviews.models import Review


class ReviewReadSerializer(serializers.ModelSerializer):
    """
    Review 的只读序列化（用于 ProductDetailSerializer 的嵌套展示）
    这里用 ModelSerializer，体现“读场景更简单”
    """

    class Meta:
        model = Review
        fields = ["id", "rating", "content", "author_display", "created_at"]
        read_only_fields = fields


class ReviewWriteSerializer(serializers.Serializer):
    """
    Serializer（非 ModelSerializer）：
    - 需要手工声明字段
    - 需要手工实现 create/update
    - 更适合：非 ORM 数据、聚合/组合输入、复杂写入逻辑

    write_only / read_only：
    - author_name（write_only）：只允许写入，不在输出出现
    - author_display（read_only）：输出展示字段，不允许客户端直接写
    """

    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()
    content = serializers.CharField()
    author_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    author_display = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate_rating(self, value: int):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating 必须在 1~5")
        return value

    def validate(self, attrs):
        """
        对象级校验示例：
        - content 最少 5 个字符
        """
        if len(attrs.get("content", "")) < 5:
            raise serializers.ValidationError({"content": "content 至少 5 个字符"})
        return attrs

    def create(self, validated_data):
        """
        手工 create：
        - 从上下文获取 product_id（由 View 注入）
        - author_name 写入到 author_display（存储字段）
        """
        product = self.context["product"]
        author_name = (validated_data.pop("author_name", "") or "").strip()
        author_display = author_name if author_name else "匿名用户"

        review = Review.objects.create(
            product=product,
            rating=validated_data["rating"],
            content=validated_data["content"],
            author_display=author_display,
        )
        return review

    def update(self, instance: Review, validated_data):
        """
        手工 update（本项目暂不开放 Review 更新接口，但完整演示 update 写法）
        """
        if "rating" in validated_data:
            instance.rating = validated_data["rating"]
        if "content" in validated_data:
            instance.content = validated_data["content"]

        if "author_name" in validated_data:
            author_name = (validated_data.get("author_name") or "").strip()
            instance.author_display = author_name if author_name else instance.author_display

        instance.save()
        return instance