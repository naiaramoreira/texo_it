from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_movies_by_title():
    response = client.get("/search_movies?title=Inception")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("Inception" in movie['title'] for movie in data)

def test_search_movies_by_year():
    response = client.get("/search_movies?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(movie['year'] == 2010 for movie in data)

def test_search_movies_by_title_and_year():
    response = client.get("/search_movies?title=Inception&year=2010")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['title'] == "Inception" and data[0]['year'] == 2010

def test_search_movies_no_results():
    response = client.get("/search_movies?title=Nonexistent Movie")
    assert response.status_code == 404

def test_add_movie():
    new_movie = {
        "year": 2020,
        "title": "Test Movie",
        "studios": "Test Studio",
        "producers": "Test Producer",
        "winner": False
    }
    response = client.post("/movies", json=new_movie)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Movie added successfully"

def test_update_movie():
    updated_movie = {
        "year": 2021,
        "title": "Test Movie Updated",
        "studios": "Test Studio Updated",
        "producers": "Test Producer Updated",
        "winner": True
    }
    response = client.put("/movies/1", json=updated_movie)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie updated successfully"

def test_delete_movie():
    response = client.delete("/movies/1")
    assert response.status_code == 204

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
