from typing import List, Optional
from pydantic import BaseModel


class DirectorOut(BaseModel):
    id: int
    name: str


class MovieOut(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    director: DirectorOut
    genres: List[str]
    average_rating: Optional[float]

    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[MovieOut]


class MovieCreate(BaseModel):
    title: str
    director_id: int
    release_year: int
    cast: Optional[str] = None
    genres: List[int]

