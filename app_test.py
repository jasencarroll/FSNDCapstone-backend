import os
import unittest
import json
from app import create_app
from models import setup_db, Movie, Actor, db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "capstone_test"
        # self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        # Sample data for testing
        self.new_movie = {
            'title': 'Test Movie',
            'release_date': '2021-01-01'
        }

        self.new_actor = {
            'name': 'Test Actor',
            'age': 30,
            'gender': 'Male'
        }

        # Tokens for different roles (Replace 'YOUR_TOKEN' with actual tokens)
        self.assistant_token = os.environ.get('ASSISTANT_TOKEN')
        self.director_token = os.environ.get('DIRECTOR_TOKEN')
        self.producer_token = os.environ.get('PRODUCER_TOKEN')
        self.invalid_token = os.environ.get('INVALID_TOKEN')

        # Bind the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # Create all tables
            self.db.create_all()

            # Ensure the database is clean before each test
            self.db.session.query(Movie).delete()
            self.db.session.query(Actor).delete()
            self.db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Tests for GET /movies
    def test_get_movies_success(self):
        """Test retrieving movies with valid token"""
        res = self.client().get('/movies', headers={'Authorization': self.assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movies'], list)

    # def test_get_movies_unauthorized(self):
    #     """Test retrieving movies with invalid token"""
    #     res = self.client().get('/movies', headers={'Authorization': self.invalid_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data['success'])

    # def test_get_movies_no_movies(self):
    #     """Test retrieving movies when none exist"""
    #     res = self.client().get('/movies', headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(len(data['movies']), 0)

    # # Tests for GET /actors
    # def test_get_actors_success(self):
    #     """Test retrieving actors with valid token"""
    #     res = self.client().get('/actors', headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertIsInstance(data['actors'], list)

    # def test_get_actors_unauthorized(self):
    #     """Test retrieving actors with invalid token"""
    #     res = self.client().get('/actors', headers={'Authorization': self.invalid_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data['success'])

    # def test_get_actors_no_actors(self):
    #     """Test retrieving actors when none exist"""
    #     res = self.client().get('/actors', headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(len(data['actors']), 0)

    # # Tests for POST /movies
    # def test_create_movie_success(self):
    #     """Test creating a new movie with valid data and token"""
    #     res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': self.producer_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 201)
    #     self.assertTrue(data['success'])
    #     self.assertIsNotNone(data['movie'])

    # def test_create_movie_missing_fields(self):
    #     """Test creating a new movie with missing fields"""
    #     res = self.client().post('/movies', json={'title': 'Incomplete Movie'}, headers={'Authorization': self.producer_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])

    # def test_create_movie_unauthorized(self):
    #     """Test creating a new movie without proper permissions"""
    #     res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # Tests for POST /actors
    # def test_create_actor_success(self):
    #     """Test creating a new actor with valid data and token"""
    #     res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 201)
    #     self.assertTrue(data['success'])
    #     self.assertIsNotNone(data['actor'])

    # def test_create_actor_missing_fields(self):
    #     """Test creating a new actor with missing fields"""
    #     res = self.client().post('/actors', json={'name': 'Incomplete Actor'}, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])

    # def test_create_actor_unauthorized(self):
    #     """Test creating a new actor without proper permissions"""
    #     res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # Tests for DELETE /movies/<int:movie_id>
    # def test_delete_movie_success(self):
    #     """Test deleting a movie with valid token"""
    #     # First, create a movie to delete
    #     movie = Movie(title='Delete Movie', release_date='2022-01-01')
    #     movie.insert()
    #     movie_id = movie.id

    #     res = self.client().delete(f'/movies/{movie_id}', headers={'Authorization': self.producer_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['deleted'], movie_id)

    # def test_delete_movie_not_found(self):
    #     """Test deleting a movie that doesn't exist"""
    #     res = self.client().delete('/movies/9999', headers={'Authorization': self.producer_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])

    # def test_delete_movie_unauthorized(self):
    #     """Test deleting a movie without proper permissions"""
    #     # First, create a movie to attempt to delete
    #     movie = Movie(title='Unauthorized Delete', release_date='2022-01-01')
    #     movie.insert()
    #     movie_id = movie.id

    #     res = self.client().delete(f'/movies/{movie_id}', headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # Tests for DELETE /actors/<int:actor_id>
    # def test_delete_actor_success(self):
    #     """Test deleting an actor with valid token"""
    #     # First, create an actor to delete
    #     actor = Actor(name='Delete Actor', age=40, gender='Female')
    #     actor.insert()
    #     actor_id = actor.id

    #     res = self.client().delete(f'/actors/{actor_id}', headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['deleted'], actor_id)

    # def test_delete_actor_not_found(self):
    #     """Test deleting an actor that doesn't exist"""
    #     res = self.client().delete('/actors/9999', headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])

    # def test_delete_actor_unauthorized(self):
    #     """Test deleting an actor without proper permissions"""
    #     # First, create an actor to attempt to delete
    #     actor = Actor(name='Unauthorized Delete', age=40, gender='Female')
    #     actor.insert()
    #     actor_id = actor.id

    #     res = self.client().delete(f'/actors/{actor_id}', headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # Tests for PATCH /movies/<int:movie_id>
    # def test_update_movie_success(self):
    #     """Test updating a movie with valid data and token"""
    #     # First, create a movie to update
    #     movie = Movie(title='Old Title', release_date='2022-01-01')
    #     movie.insert()
    #     movie_id = movie.id

    #     res = self.client().patch(f'/movies/{movie_id}', json={'title': 'New Title'}, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)
    #     updated_movie = Movie.query.get(movie_id)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(updated_movie.title, 'New Title')

    # def test_update_movie_not_found(self):
    #     """Test updating a movie that doesn't exist"""
    #     res = self.client().patch('/movies/9999', json={'title': 'New Title'}, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])

    # def test_update_movie_unauthorized(self):
    #     """Test updating a movie without proper permissions"""
    #     # First, create a movie to attempt to update
    #     movie = Movie(title='Unauthorized Update', release_date='2022-01-01')
    #     movie.insert()
    #     movie_id = movie.id

    #     res = self.client().patch(f'/movies/{movie_id}', json={'title': 'New Title'}, headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # Tests for PATCH /actors/<int:actor_id>
    # def test_update_actor_success(self):
    #     """Test updating an actor with valid data and token"""
    #     # First, create an actor to update
    #     actor = Actor(name='Old Name', age=30, gender='Male')
    #     actor.insert()
    #     actor_id = actor.id

    #     res = self.client().patch(f'/actors/{actor_id}', json={'name': 'New Name'}, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)
    #     updated_actor = Actor.query.get(actor_id)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(updated_actor.name, 'New Name')

    # def test_update_actor_not_found(self):
    #     """Test updating an actor that doesn't exist"""
    #     res = self.client().patch('/actors/9999', json={'name': 'New Name'}, headers={'Authorization': self.director_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])

    # def test_update_actor_unauthorized(self):
    #     """Test updating an actor without proper permissions"""
    #     # First, create an actor to attempt to update
    #     actor = Actor(name='Unauthorized Update', age=30, gender='Male')
    #     actor.insert()
    #     actor_id = actor.id

    #     res = self.client().patch(f'/actors/{actor_id}', json={'name': 'New Name'}, headers={'Authorization': self.assistant_token})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
