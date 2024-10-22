import os
import unittest
import json
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

BASE_URL = 'http://localhost:5000'

# Replace these with actual JWT tokens for each role
ASSISTANT_TOKEN=os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN=os.environ.get('CASTING_DIRECTOR_TOKEN')
PRODUCER_TOKEN=os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the test cases for the Casting Agency API"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.movie = {
            'title': 'Test Movie',
            'release_date': '2023-10-10'
        }
        self.actor = {
            'name': 'Test Actor',
            'age': 30,
            'gender': 'Male'
        }

    def test(self):
        response = requests.get(f'{BASE_URL}')
        self.assertEqual(response.status_code, 200)

    # Success behavior tests for each endpoint
    def test_get_movies_success(self):
        headers = {
            'authorization': f'Bearer {DIRECTOR_TOKEN}'
        }
        response = requests.get(f'{BASE_URL}/movies', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_actors_success(self):
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}'
        }
        response = requests.get(f'{BASE_URL}/actors', headers=headers)
        self.assertEqual(response.status_code, 200)

    # def test_post_movie_success(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
    #     self.assertEqual(response.status_code, 201)

    # def test_post_actor_success(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
    #     self.assertEqual(response.status_code, 201)

    # def test_patch_movie_success(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     # First, create a movie to update
    #     post_response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
    #     movie_id = post_response.json()['movie']['id']
    #     # Now, update the movie
    #     update_data = {'title': 'Updated Test Movie'}
    #     response = requests.patch(f'{BASE_URL}/movies/{movie_id}', headers=headers, data=json.dumps(update_data))
    #     self.assertEqual(response.status_code, 200)

    # def test_patch_actor_success(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     # First, create an actor to update
    #     post_response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
    #     actor_id = post_response.json()['actor']['id']
    #     # Now, update the actor
    #     update_data = {'age': 35}
    #     response = requests.patch(f'{BASE_URL}/actors/{actor_id}', headers=headers, data=json.dumps(update_data))
    #     self.assertEqual(response.status_code, 200)

    # def test_delete_movie_success(self):
    #     headers = {'Authorization': EXECUTIVE_PRODUCER_TOKEN}
    #     # First, create a movie to delete
    #     post_response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
    #     movie_id = post_response.json()['movie']['id']
    #     # Now, delete the movie
    #     response = requests.delete(f'{BASE_URL}/movies/{movie_id}', headers=headers)
    #     self.assertEqual(response.status_code, 200)

    # def test_delete_actor_success(self):
    #     headers = {'Authorization': EXECUTIVE_PRODUCER_TOKEN}
    #     # First, create an actor to delete
    #     post_response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
    #     actor_id = post_response.json()['actor']['id']
    #     # Now, delete the actor
    #     response = requests.delete(f'{BASE_URL}/actors/{actor_id}', headers=headers)
    #     self.assertEqual(response.status_code, 200)

    # # Error behavior tests for each endpoint

    # def test_get_movies_unauthorized(self):
    #     headers = {}  # No Authorization header
    #     response = requests.get(f'{BASE_URL}/movies', headers=headers)
    #     self.assertEqual(response.status_code, 401)

    # def test_get_actors_unauthorized(self):
    #     headers = {}  # No Authorization header
    #     response = requests.get(f'{BASE_URL}/actors', headers=headers)
    #     self.assertEqual(response.status_code, 401)

    # def test_post_movie_unprocessable(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     incomplete_movie = {'title': 'Incomplete Movie'}
    #     response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(incomplete_movie))
    #     self.assertEqual(response.status_code, 422)

    # def test_post_actor_unprocessable(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     incomplete_actor = {'name': 'Incomplete Actor'}
    #     response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(incomplete_actor))
    #     self.assertEqual(response.status_code, 422)

    # def test_patch_movie_not_found(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.patch(f'{BASE_URL}/movies/9999', headers=headers, data=json.dumps({'title': 'Does not exist'}))
    #     self.assertEqual(response.status_code, 404)

    # def test_patch_actor_not_found(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.patch(f'{BASE_URL}/actors/9999', headers=headers, data=json.dumps({'age': 100}))
    #     self.assertEqual(response.status_code, 404)

    # def test_delete_movie_not_found(self):
    #     headers = {'Authorization': EXECUTIVE_PRODUCER_TOKEN}
    #     response = requests.delete(f'{BASE_URL}/movies/9999', headers=headers)
    #     self.assertEqual(response.status_code, 404)

    # def test_delete_actor_not_found(self):
    #     headers = {'Authorization': EXECUTIVE_PRODUCER_TOKEN}
    #     response = requests.delete(f'{BASE_URL}/actors/9999', headers=headers)
    #     self.assertEqual(response.status_code, 404)

    # # RBAC tests for each role (at least two tests per role)

    # # Casting Assistant tests
    # def test_casting_assistant_get_movies(self):
    #     headers = {'Authorization': CASTING_ASSISTANT_TOKEN}
    #     response = requests.get(f'{BASE_URL}/movies', headers=headers)
    #     self.assertEqual(response.status_code, 200)

    # def test_casting_assistant_delete_actor_forbidden(self):
    #     headers = {'Authorization': CASTING_ASSISTANT_TOKEN}
    #     response = requests.delete(f'{BASE_URL}/actors/1', headers=headers)
    #     self.assertEqual(response.status_code, 403)

    # # Casting Director tests
    # def test_casting_director_add_actor(self):
    #     headers = {
    #         'Authorization': CASTING_DIRECTOR_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
    #     self.assertEqual(response.status_code, 201)

    # def test_casting_director_delete_movie_forbidden(self):
    #     headers = {'Authorization': CASTING_DIRECTOR_TOKEN}
    #     response = requests.delete(f'{BASE_URL}/movies/1', headers=headers)
    #     self.assertEqual(response.status_code, 403)

    # # Executive Producer tests
    # def test_executive_producer_add_movie(self):
    #     headers = {
    #         'Authorization': EXECUTIVE_PRODUCER_TOKEN,
    #         'Content-Type': 'application/json'
    #     }
    #     response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
    #     self.assertEqual(response.status_code, 201)

    # def test_executive_producer_delete_actor(self):
    #     headers = {'Authorization': EXECUTIVE_PRODUCER_TOKEN}
    #     # First, create an actor to delete
    #     post_response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
    #     actor_id = post_response.json()['actor']['id']
    #     # Now, delete the actor
    #     response = requests.delete(f'{BASE_URL}/actors/{actor_id}', headers=headers)
    #     self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
