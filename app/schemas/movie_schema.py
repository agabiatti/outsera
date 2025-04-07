from pydantic import BaseModel
from typing import List

class MovieCreate(BaseModel):
    release_year: int
    title: str
    winner: bool

class MovieFullCreate(BaseModel):
    title: str
    release_year: int
    winner: bool
    producers: List[str]
    studios: List[str]

class MovieOut(MovieCreate):
    id: int

    model_config = {
        "from_attributes": True
    }