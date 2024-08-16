from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db
from logger import get_logger

logger = get_logger(__name__)

app = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@app.post("/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user} is creating a comment")
    movie = db.query(models.Movie).filter(models.Movie.id == comment.movie_id).first()
    if not movie:
        logger.error("movie cannot be found")
        raise HTTPException(status_code=404, detail="Movie not found")

    db_comment = models.Comment(**comment.dict(), user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/", response_model=List[schemas.Comment])
def get_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Current user wants to get {comments}")
    comments = db.query(models.Comment).offset(skip).limit(limit).all()
    return comments
