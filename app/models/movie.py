from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.genres_movie import genres_movie

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id", ondelete="RESTRICT"), nullable=False)
    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cast: Mapped[str | None] = mapped_column(String(500), nullable=True)

    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=genres_movie, back_populates="movies")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")
