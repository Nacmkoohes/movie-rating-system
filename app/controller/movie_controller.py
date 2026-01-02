from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.movie_service import MovieService
from app.schemas.rating import RatingCreate
from app.services.rating_service import RatingService
from app.schemas.movie import MovieCreate

import logging

logger = logging.getLogger("movie_rating")

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])


@router.get("/", response_model=dict, operation_id="list_movies")
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    logger.info("Fetching movie list")

    try:
        data = MovieService.list_movies(db=db, page=page, limit=limit)
        logger.info(f"Fetched {len(data['items'])} movies successfully")
        return {"status": "success", "data": data}
    except Exception:
        logger.error("Failed to fetch movie list", exc_info=True)
        raise



@router.get("/{movie_id}", response_model=dict, operation_id="get_movie")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    data = MovieService.get_movie_details(db=db, movie_id=movie_id)
    return {"status": "success", "data": data}

@router.post("/{movie_id}/ratings", response_model=dict, operation_id="add_movie_rating")
def add_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):
    data = RatingService.add_rating(db=db, movie_id=movie_id, score=payload.score)
    return {"status": "success", "data": data}


@router.post("/", operation_id="create_movie")
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    data = MovieService.create_movie(db=db, payload=payload)
    return {"status": "success", "data": data}

@router.put("/{movie_id}", operation_id="update_movie")
def update_movie(
    movie_id: int,
    payload: MovieCreate,
    db: Session = Depends(get_db),
):
    data = MovieService.update_movie(db, movie_id, payload)
    return {"status": "success", "data": data}

@router.delete("/{movie_id}", status_code=204, operation_id="delete_movie")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    MovieService.delete_movie(db, movie_id)


@router.post(
    "/{movie_id}/ratings",
    response_model=dict,
    operation_id="add_movie_rating"
)
def add_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):

    logger.info(
        f"Add rating request (movie_id={movie_id}, score={payload.score}, route=/api/v1/movies/{movie_id}/ratings)"
    )

    if payload.score < 1 or payload.score > 10:
        logger.warning(
            f"Invalid rating score (movie_id={movie_id}, score={payload.score})"
        )
        raise HTTPException(status_code=400, detail="Invalid rating score")

    try:
        data = RatingService.add_rating(
            db=db,
            movie_id=movie_id,
            score=payload.score
        )
        logger.info(
            f"Rating added successfully (movie_id={movie_id}, score={payload.score})"
        )
        return {"status": "success", "data": data}

    except Exception:
        logger.error(
            f"Failed to add rating (movie_id={movie_id}, score={payload.score})",
            exc_info=True
        )
        raise
