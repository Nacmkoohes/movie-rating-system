from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.movie import Movie
from app.models.movie_rating import MovieRating


class RatingRepository:
    @staticmethod
    def movie_exists(db: Session, movie_id: int) -> bool:
        return db.query(Movie.id).filter(Movie.id == movie_id).first() is not None

    @staticmethod
    def create_rating(db: Session, movie_id: int, score: int) -> MovieRating:
        rating = MovieRating(movie_id=movie_id, score=score)
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating

    @staticmethod
    def get_movie_avg_rating(db: Session, movie_id: int):
        return (
            db.query(func.avg(MovieRating.score))
            .filter(MovieRating.movie_id == movie_id)
            .scalar()
        )
