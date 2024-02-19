from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi import Query
from database import database
from typing import Optional

app = FastAPI(title="Movie Awards API")

class Movie(BaseModel):
    year: int
    title: str
    studios: str
    producers: str
    winner: Optional[bool] = False

@app.on_event("startup")
async def startup_event():
    database.create_movies_table()

@app.post("/movies")
async def add_movie(movie: Movie):
    database.add_movie(movie)
    return {"message": "Movie added successfully"}

@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie: Movie):
    updated_rows = database.update_movie(movie_id, movie)
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie updated successfully"}

@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int):
    deleted_rows = database.delete_movie(movie_id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

@app.get("/movies")
async def list_movies():
    movies = database.get_movies()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    return movies

@app.get("/search_movies")
async def search_movies(title: Optional[str] = None, year: Optional[int] = None):
    movies = database.get_movie_by_title_or_year(title, year)
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found matching the criteria")
    return movies

@app.get("/producers/intervals")
async def get_producer_intervals():
    intervals = database.calculate_intervals()
    return intervals


@app.get("/healthcheck", status_code=200)
def healthcheck():
    return {"status": "UP"}
