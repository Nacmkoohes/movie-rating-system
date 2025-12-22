from pydantic import BaseModel, Field

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=10)
