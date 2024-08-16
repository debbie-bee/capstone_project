from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db
from models import Rating, User, Movie
from logger import get_logger

logger = get_logger(__name__)

app = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)

@app.post("/", response_model=schemas.Rating)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user} giving rating: {create_rating}")
    
    movie = db.query(models.Movie).filter(models.Movie.id == rating.movie_id).first()
    if not movie:
        logger.error(f"{movie.id} doesn't exist")
        raise HTTPException(status_code=404, detail="Movie not found")
    
    existing_rating = db.query(Rating).filter(Rating.movie_id == rating.movie_id, Rating.user_id == current_user.id).first()
    if existing_rating:
        logger.warning(f"user is trying to create rating but it exists: {existing_rating}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this movie")

    db_rating = models.Rating(**rating.dict(), user_id=current_user.id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.get("/", response_model=List[schemas.Rating])
def get_ratings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("user getting rating...")
    ratings = db.query(models.Rating).offset(skip).limit(limit).all()
    return ratings
