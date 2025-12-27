from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.genre import Genre
from app.models.movie import Movie
from app.models.movie_rating import MovieRating


class MovieRepository:
    @staticmethod
    def count_movies(db: Session) -> int:
        return db.query(Movie).count()

    @staticmethod
    def list_movies_with_avg_rating(db: Session, offset: int, limit: int):
        """
        Returns: list of tuples -> (Movie, avg_rating)
        avg_rating can be None if a movie has no ratings.
        """
        return (
            db.query(Movie, func.avg(MovieRating.score).label("avg_rating"))
            .outerjoin(MovieRating, MovieRating.movie_id == Movie.id)
            .group_by(Movie.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_movie_with_avg_rating(db: Session, movie_id: int):
        """
        Returns: tuple -> (Movie, avg_rating) or None
        """
        return (
            db.query(Movie, func.avg(MovieRating.score).label("avg_rating"))
            .outerjoin(MovieRating, MovieRating.movie_id == Movie.id)
            .filter(Movie.id == movie_id)
            .group_by(Movie.id)
            .first()
        )

    @staticmethod
    def create_movie(db: Session, movie: Movie):
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie

    @staticmethod
    def get_genres_by_ids(db: Session, genre_ids: list[int]):
        return db.query(Genre).filter(Genre.id.in_(genre_ids)).all()

    @staticmethod
    def delete_movie(db: Session, movie: Movie):
        db.delete(movie)
        db.commit()
