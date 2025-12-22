from sqlalchemy.orm import Session
from app.models.genre import Genre


class GenreRepository:
    @staticmethod
    def list_genres(db: Session):
        return db.query(Genre).order_by(Genre.name).all()
