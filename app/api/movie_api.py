from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers.movie_controller import MovieController
from app.schemas.movie_schema import MovieCreate, MovieFullCreate, MovieOut
from app.connections.db import get_db

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieOut)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    result = MovieController(db).create_movie(movie)
    
    return result

@router.get("/", response_model=list[MovieOut])
def read_movies(db: Session = Depends(get_db)):
    results = MovieController(db).read_movies()

    if len(results) > 0:
        return results

    raise HTTPException(status_code=404, detail="Movies not found")

@router.get("/{movie_id}", response_model=MovieOut)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    result = MovieController(db).read_movie(movie_id)

    if result:
        return result

    raise HTTPException(status_code=404, detail="Movie not found")

@router.put("/{movie_id}", response_model=MovieOut)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    result = MovieController(db).update_movie(movie_id, movie)

    if result:
        return result    
    
    raise HTTPException(status_code=404, detail="Movie not found")

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    result = MovieController(db).update_movie(movie_id)

    if result:
        return {"message": "Movie deleted"}
    
    raise HTTPException(status_code=404, detail="Movie not found")

@router.post("/full-create", response_model=MovieFullCreate)
def create_movie_with_associations(movie_data: MovieFullCreate, db: Session = Depends(get_db)):
    result = MovieController(db).create_movie_with_associations(movie_data)

    if result:
        return result
    
    raise HTTPException(status_code=500, detail="Movie not created")