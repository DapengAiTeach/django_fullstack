import os
import random
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

from apps.movies.models import (  # noqa: E402
    Country,
    Genre,
    Language,
    Movie,
    MovieCredit,
    Person,
)


def ensure_user(username, password, is_staff=False, is_superuser=False):
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"is_staff": is_staff, "is_superuser": is_superuser},
    )
    if not created:
        user.is_staff = is_staff
        user.is_superuser = is_superuser
    user.set_password(password)
    user.save()
    return user


def seed_reference_data():
    genres = ["剧情", "喜剧", "动作", "科幻", "动画", "爱情", "悬疑", "犯罪"]
    countries = ["中国", "日本", "美国", "英国", "法国"]
    languages = ["中文", "日语", "英语"]

    genre_objs = [Genre.objects.get_or_create(name=name)[0] for name in genres]
    country_objs = [Country.objects.get_or_create(name=name)[0] for name in countries]
    language_objs = [Language.objects.get_or_create(name=name)[0] for name in languages]

    people = [
        ("阪元裕吾", "Yugo Sakamoto"),
        ("石黑正数", "Masakazu Ishiguro"),
        ("久保史绪里", "Shiori Kubo"),
        ("平祐奈", "Yuna Taira"),
        ("纲启永", "Keito Tsuna"),
        ("樋口幸平", "Kohei Higuchi"),
        ("张三", "Zhang San"),
        ("李四", "Li Si"),
    ]
    person_objs = [
        Person.objects.get_or_create(name_cn=cn, defaults={"name_en": en})[0]
        for cn, en in people
    ]

    return genre_objs, country_objs, language_objs, person_objs


def seed_movies(
    total=100,
    genres=None,
    countries=None,
    languages=None,
    people=None,
):
    random.seed(42)
    subtitles = ["中文", "英文", "日文", "无"]

    directors = people[:2]
    writers = people[2:4]
    actors = people[4:]

    for i in range(1, total + 1):
        title_cn = f"电影 {i:03d}"
        title_original = f"Movie {i:03d}"
        year = random.randint(2018, 2025)
        release_date = date(year, random.randint(1, 12), random.randint(1, 28))
        publish_date = date(2025, 11, 4)
        duration_minutes = random.randint(80, 150)
        imdb_rating = Decimal(str(round(random.uniform(6.0, 8.5), 1)))
        douban_rating = Decimal(str(round(random.uniform(6.0, 8.8), 1)))
        price = Decimal(str(round(random.uniform(19.9, 99.9), 2)))

        movie, created = Movie.objects.get_or_create(
            title_cn=title_cn,
            defaults={
                "title_original": title_original,
                "year": year,
                "genre": random.choice(genres),
                "country": random.choice(countries),
                "language": random.choice(languages),
                "subtitle": random.choice(subtitles),
                "release_date": release_date,
                "publish_date": publish_date,
                "imdb_rating": imdb_rating,
                "imdb_votes": random.randint(50, 5000),
                "douban_rating": douban_rating,
                "douban_votes": random.randint(200, 50000),
                "duration_minutes": duration_minutes,
                "summary": f"Sample summary for movie {i:03d}.",
                "price": price,
                "stock": random.randint(0, 200),
                "is_on_sale": random.choice([True, True, True, False]),
                "is_hot": random.choice([True, False]),
            },
        )

        if created or not movie.credits.exists():
            MovieCredit.objects.filter(movie=movie).delete()
            director = random.choice(directors)
            writer = random.choice(writers)
            actor_list = random.sample(actors, k=min(3, len(actors)))

            MovieCredit.objects.create(
                movie=movie, person=director, role=MovieCredit.ROLE_DIRECTOR, sort=1
            )
            MovieCredit.objects.create(
                movie=movie, person=writer, role=MovieCredit.ROLE_WRITER, sort=1
            )
            for idx, actor in enumerate(actor_list, start=1):
                MovieCredit.objects.create(
                    movie=movie, person=actor, role=MovieCredit.ROLE_ACTOR, sort=idx
                )


def main():
    ensure_user("admin", "admin123456", is_staff=True, is_superuser=True)
    ensure_user("test", "test123456", is_staff=False, is_superuser=False)

    genres, countries, languages, people = seed_reference_data()
    seed_movies(
        total=100,
        genres=genres,
        countries=countries,
        languages=languages,
        people=people,
    )

    print("Init data completed.")


if __name__ == "__main__":
    main()
