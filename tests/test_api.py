import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_search_movies_by_title(self):
        response = self.client.get("/search_movies?title=Inception")
        self.assertEqual(response.status_code, 404)

    def test_search_movies_by_year(self):
        response = self.client.get("/search_movies?year=1990")
        self.assertEqual(response.status_code, 200)

    def test_search_movies_by_title_and_year(self):
        response = self.client.get("/search_movies?title=Inception&year=1900")
        self.assertEqual(response.status_code, 404)

    def test_search_movies_no_results(self):
        response = self.client.get("/search_movies?title=Nonexistent Movie")
        self.assertEqual(response.status_code, 404)

    def test_add_movie(self):
        new_movie = {
            "year": 2020,
            "title": "Test Movie",
            "studios": "Test Studio",
            "producers": "Test Producer",
            "winner": False
        }
        response = self.client.post("/movies", json=new_movie)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Movie added successfully")

    def test_update_movie(self):
        updated_movie = {
            "year": 2021,
            "title": "Test Movie Updated",
            "studios": "Test Studio Updated",
            "producers": "Test Producer Updated",
            "winner": True
        }
        response = self.client.put("/movies/1", json=updated_movie)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Movie updated successfully")

    def test_delete_movie(self):
        response = self.client.delete("/movies/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Movie deleted successfully")

    def test_get_movies(self):
        response = self.client.get("/movies")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_get_producer_intervals(self):
        response = client.get("/producers/intervals")
        self.assertEqual(response.status_code, 200, "Expected status code 200")

        data = response.json()

        self.assertIn('min', data, "'min' key is missing in the response")
        self.assertIn('max', data, "'max' key is missing in the response")

        self.assertIsInstance(data['min'], list, "'min' should be a list")
        self.assertIsInstance(data['max'], list, "'max' should be a list")

        self.assertGreater(len(data['min']), 0, "'min' list is empty")
        self.assertGreater(len(data['max']), 0, "'max' list is empty")

        for interval in data['min'] + data['max']:
            self.assertIn('producers', interval, "'producers' key is missing in an interval")
            self.assertIn('interval', interval, "'interval' key is missing in an interval")
            self.assertIn('previousWin', interval, "'previousWin' key is missing in an interval")
            self.assertIn('followingWin', interval, "'followingWin' key is missing in an interval")
            self.assertIsInstance(interval['interval'], int, "'interval' should be an integer")

if __name__ == "__main__":
    unittest.main()
