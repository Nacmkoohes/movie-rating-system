from fastapi import FastAPI
from app.controller.movie_controller import router as movie_router

app = FastAPI(title="Movie Rating System")

app.include_router(movie_router)
