import unittest

from werkzeug.exceptions import HTTPException
import movies
import models

class TestMovies(unittest.TestCase):
    def setUp(self):
        # Load test data
        self.app = models.Movies

    def test_movie(self):
        movie, status = movies.read_one(7111, 48401)
        self.assertEqual(movie['title'], 'Good')
        self.assertEqual(status, 200)