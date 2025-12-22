from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.rating_repository import RatingRepository


class RatingService:
    @staticmethod
    def add_rating(db: Session, movie_id: int, score: int) -> dict:
        if not RatingRepository.movie_exists(db=db, movie_id=movie_id):
            raise HTTPException(status_code=404, detail="Movie not found")

        rating = RatingRepository.create_rating(db=db, movie_id=movie_id, score=score)
        avg = RatingRepository.get_movie_avg_rating(db=db, movie_id=movie_id)

        return {
            "rating_id": rating.id,
            "movie_id": movie_id,
            "score": rating.score,
            "average_rating": round(float(avg), 2) if avg is not None else None,
        }
