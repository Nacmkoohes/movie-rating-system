from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.movie_service import MovieService

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])


@router.get("/", response_model=dict)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    data = MovieService.list_movies(db=db, page=page, page_size=page_size)
    return {"status": "success", "data": data}
