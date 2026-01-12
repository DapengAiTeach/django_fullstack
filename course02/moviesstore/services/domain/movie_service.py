from apps.content.models import Movie, MovieAsset
from services.common.exceptions import NotFound


class MovieService:

    @staticmethod
    def create_movie(data: dict) -> Movie:
        return Movie.objects.create(**data)

    @staticmethod
    def update_movie(movie_id: int, data: dict) -> Movie:
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            raise NotFound("电影不存在")
        for k, v in data.items():
            setattr(movie, k, v)
        movie.save()
        return movie

    @staticmethod
    def set_status(movie_id: int, status: str):
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            raise NotFound("电影不存在")
        movie.status = status
        movie.save(update_fields=["status"])

    @staticmethod
    def add_asset(movie: Movie, asset_type: str, url: str, is_primary=False):
        if is_primary:
            MovieAsset.objects.filter(movie=movie, asset_type=asset_type).update(is_primary=False)
        return MovieAsset.objects.create(
            movie=movie,
            asset_type=asset_type,
            url=url,
            is_primary=is_primary,
        )