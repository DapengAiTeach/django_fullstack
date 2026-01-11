from rest_framework import serializers
from apps.articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "author_id", "title", "content", "is_published", "is_locked", "created_at", "updated_at"]
        read_only_fields = ["id", "author_id", "is_locked", "created_at", "updated_at"]

    def validate_title(self, value: str):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("title 长度至少 3")
        return value