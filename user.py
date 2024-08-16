from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas
import crud
import auth
from database import get_db
from logger import get_logger

logger = get_logger(__name__)

app = APIRouter(
    prefix="/users",
    tags=["users"],
)


@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("creating user.......")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(
            f"user is trying to register but email already exists:{user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login")
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("getting user....")
    db_user = auth.authenticate_user(
        db, email=user.email, password=user.password)
    if not db_user:
        logger.error("the email or password is incorrect")
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
