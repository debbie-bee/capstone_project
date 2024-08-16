from fastapi import FastAPI
from routers import user, movie, rating, comment
from logger import get_logger

app = FastAPI()

# Include routers for different endpoints
app.include_router(user.app)
app.include_router(movie.app)
app.include_router(rating.app)
app.include_router(comment.app)
