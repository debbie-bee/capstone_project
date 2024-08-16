from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db
from logger import get_logger

from auth import get_current_user

logger = get_logger(__name__)

app = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@app.post("/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    logger.info(f"User {get_current_user} creating a movie{movie.title}")
    return crud.create_movie(db=db, movie=movie, user_id=user.id)


@app.get("/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("Fetching list of movies")
    movies = crud.get_movies(db=db)
    return movies


@app.get("/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    logger.info("Fetching your movie")
    db_movie = crud.get_movie(db=db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    logger.warning("User is about to delete a movie")
    result = crud.delete_movie(
        db=db, movie_id=movie_id, user_id=current_user.id)
    if not result:
        raise HTTPException(
            status_code=400, detail="Not authorized to delete this movie")
    return {"message": "Movie deleted successfully"}
