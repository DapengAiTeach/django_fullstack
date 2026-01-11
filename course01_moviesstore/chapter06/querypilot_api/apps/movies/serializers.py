from rest_framework import serializers
from apps.movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "genre", "year", "rating", "is_hot", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("rating 必须在 0~10")
        return value