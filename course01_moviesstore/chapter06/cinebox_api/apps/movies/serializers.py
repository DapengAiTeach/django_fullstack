from rest_framework import serializers
from apps.movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer 的核心价值：
    - 把 Django Model 转换为 JSON（序列化）
    - 把 JSON 转换为可写入 Model 的数据（反序列化）
    - 负责校验（比 Django Form 更适合 API）
    """

    class Meta:
        model = Movie
        fields = ["id", "title", "overview", "release_date", "rating", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_rating(self, value):
        """
        字段级校验示例：评分必须在 0~10 之间
        """
        if value < 0 or value > 10:
            raise serializers.ValidationError("rating 必须在 0~10 之间")
        return value