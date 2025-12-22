from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.movie import Movie
from app.models.movie_rating import MovieRating


class MovieRepository:
    @staticmethod
    def count_movies(db: Session) -> int:
        return db.query(Movie).count()

    @staticmethod
    def list_movies_with_avg_rating(db: Session, offset: int, limit: int):
        # returns list of (Movie, avg_rating)
        return (
            db.query(Movie, func.avg(MovieRating.score).label("avg_rating"))
            .outerjoin(MovieRating, MovieRating.movie_id == Movie.id)
            .group_by(Movie.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
