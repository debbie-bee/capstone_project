from pydantic import BaseModel
# from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True #shows an orm configuration

class MovieCreate(BaseModel):
    title: str
    description: str

class Movie(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    content: str
    movie_id: int
    user_id: int
    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    score: int

class Rating(BaseModel):
    id: int
    score: int
    movie_id: int
    user_id: int
    class Config:
        from_attributes = True
