from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.model_dump(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session):
    return db.query(models.Movie).all()

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, movie_id: int):
    db_comment = models.Comment(**comment.dict(), user_id=user_id, movie_id=movie_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_rating(db: Session, rating: schemas.RatingCreate, user_id: int, movie_id: int):
    db_rating = models.Rating(**rating.dict(), user_id=user_id, movie_id=movie_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()


def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate, user_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie and db_movie.owner_id == user_id:
        db_movie.title = movie.title
        db_movie.description = movie.description
        db.commit()
        db.refresh(db_movie)
        return db_movie
    return None

def delete_movie(db: Session, movie_id: int, user_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie and db_movie.owner_id == user_id:
        db.delete(db_movie)
        db.commit()
        return True
    return False