from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate
from app.models.movie import Movie


class MovieService:
    @staticmethod
    def list_movies(db: Session, page: int, page_size: int) -> dict:
        offset = (page - 1) * page_size

        total_items = MovieRepository.count_movies(db)
        rows = MovieRepository.list_movies_with_avg_rating(db=db, offset=offset, limit=page_size)

        items = []
        for movie, avg_rating in rows:
            items.append(
                {
                    "id": movie.id,
                    "title": movie.title,
                    "release_year": movie.release_year,
                    "director": {"id": movie.director.id, "name": movie.director.name},
                    "genres": [g.name for g in movie.genres],
                    "average_rating": round(float(avg_rating), 2) if avg_rating is not None else None,
                }
            )

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "items": items,
        }

    @staticmethod
    def get_movie_details(db: Session, movie_id: int) -> dict:
        row = MovieRepository.get_movie_with_avg_rating(db=db, movie_id=movie_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Movie not found")

        movie, avg_rating = row
        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {"id": movie.director.id, "name": movie.director.name},
            "genres": [g.name for g in movie.genres],
            "average_rating": round(float(avg_rating), 2) if avg_rating is not None else None,
        }


    @staticmethod
    def create_movie(db: Session, payload: MovieCreate):
        genres = MovieRepository.get_genres_by_ids(db, payload.genres)
        if len(genres) != len(payload.genres):
            raise HTTPException(status_code=422, detail="Invalid genres")

        movie = Movie(
            title=payload.title,
            director_id=payload.director_id,
            release_year=payload.release_year,
            cast=payload.cast,
        )

        movie.genres = genres
        MovieRepository.create_movie(db, movie)

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {
                "id": movie.director.id,
                "name": movie.director.name,
            },
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": None,
            "ratings_count": 0,
        }

