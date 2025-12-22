from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.movie_service import MovieService
from app.schemas.rating import RatingCreate
from app.services.rating_service import RatingService


router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])


@router.get("/", response_model=dict, operation_id="list_movies")
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    data = MovieService.list_movies(db=db, page=page, page_size=page_size)
    return {"status": "success", "data": data}


@router.get("/{movie_id}", response_model=dict, operation_id="get_movie")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    data = MovieService.get_movie_details(db=db, movie_id=movie_id)
    return {"status": "success", "data": data}

@router.post("/{movie_id}/ratings", response_model=dict, operation_id="add_movie_rating")
def add_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):
    data = RatingService.add_rating(db=db, movie_id=movie_id, score=payload.score)
    return {"status": "success", "data": data}
