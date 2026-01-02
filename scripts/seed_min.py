from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie

import sys
from pathlib import Path

sys.path.append(str(Path().resolve().parent.parent))


def seed(db: Session) -> None:

    if db.query(Movie).count() > 0:
        print("Seed skipped: movies already exist.")
        return

    nolan = Director(name="Christopher Nolan", birth_year=1970, description="Director")
    villeneuve = Director(name="Denis Villeneuve", birth_year=1967, description="Director")

    action = Genre(name="Action", description="Action films")
    scifi = Genre(name="Sci-Fi", description="Science fiction films")

    inception = Movie(title="Inception", director=nolan, release_year=2010, cast="Leonardo DiCaprio")
    inception.genres = [action, scifi]

    dune = Movie(title="Dune", director=villeneuve, release_year=2021, cast="Timothée Chalamet")
    dune.genres = [scifi]

    db.add_all([nolan, villeneuve, action, scifi, inception, dune])
    db.commit()
    print("Seed OK")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
