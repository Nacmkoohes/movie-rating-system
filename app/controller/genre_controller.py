from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.genre_service import GenreService

router = APIRouter(prefix="/api/v1/genres", tags=["Genres"])


@router.get("/", response_model=dict, operation_id="list_genres")
def list_genres(db: Session = Depends(get_db)):
    data = GenreService.list_genres(db=db)
    return {"status": "success", "data": data}
