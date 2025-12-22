from sqlalchemy.orm import Session
from app.repositories.genre_repository import GenreRepository


class GenreService:
    @staticmethod
    def list_genres(db: Session) -> list[dict]:
        genres = GenreRepository.list_genres(db)

        return [
            {
                "id": genre.id,
                "name": genre.name,
                "description": genre.description,
            }
            for genre in genres
        ]
