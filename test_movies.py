import unittest
import movies
import models

class TestMovies(unittest.TestCase):
    def setUp(self):
        """
        Inisialisasi
        """
        self.app = models.Movies

    def test_movie(self):
        """
        Testing ambil 1 data movies apakah id dan title sesuai
        serta status code nya 200 ketika berhasil
        """
        movie, status = movies.read_one(7111, 48401)
        self.assertEqual(movie['title'], 'Good')
        self.assertEqual(status, 200)
