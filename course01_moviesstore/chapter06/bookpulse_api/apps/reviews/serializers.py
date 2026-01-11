from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer（序列化器）负责：
    - 输出：Review -> JSON
    - 输入：JSON -> 校验 -> Review
    """

    class Meta:
        model = Review
        fields = ["id", "book_title", "content", "rating", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_rating(self, value: int):
        """
        字段级校验：评分必须在 1~5
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("评分必须在 1~5")
        return value