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

# ----------------------------------------
# 1. Success Behavior Tests for Each Endpoint
# ----------------------------------------

    # 1.1 Test GET /movies success
    def test_get_movies_success(self):
        """Test that a Casting Director can successfully retrieve movies."""
        headers = {
            'authorization': f'Bearer {DIRECTOR_TOKEN}'
        }
        response = requests.get(f'{BASE_URL}/movies', headers=headers)
        self.assertEqual(response.status_code, 200)

    # 1.2 Test GET /actors success
    def test_get_actors_success(self):
        """Test that an Executive Producer can successfully retrieve actors."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}'
        }
        response = requests.get(f'{BASE_URL}/actors', headers=headers)
        self.assertEqual(response.status_code, 200)

    # 1.3 Test POST /movies success
    def test_post_movie_success(self):
        """Test that an Executive Producer can successfully create a new movie."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'content-type': 'application/json'
        }

        # Temporarily hardcode the payload
        movie_data = {
            'title': 'Test Movie',
            'release_date': '2023-10-10'
        }
        
        #print(f"Sending movie data: {movie_data}")
        
        response = requests.post(f'{BASE_URL}/movies', headers=headers, json=movie_data)
        
        #print(f"Response status code: {response.status_code}")
        #print(f"Response content: {response.content.decode()}")

        self.assertEqual(response.status_code, 201)



    # 1.4 Test POST /actors success
    def test_post_actor_success(self):
        """Test that an Executive Producer can successfully create a new actor."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
        self.assertEqual(response.status_code, 201)

    # 1.5 Test PATCH /movies success
    def test_patch_movie_success(self):
        """Test that an Executive Producer can successfully update a movie."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        # First, create a movie to update
        post_response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
        movie_id = post_response.json()['movie']['id']
        # Now, update the movie
        update_data = {'title': 'Updated Test Movie'}
        response = requests.patch(f'{BASE_URL}/movies/{movie_id}', headers=headers, data=json.dumps(update_data))
        self.assertEqual(response.status_code, 200)

    # 1.6 Test PATCH /actors success
    def test_patch_actor_success(self):
        """Test that an Executive Producer can successfully update an actor."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        # First, create an actor to update
        post_response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
        actor_id = post_response.json()['actor']['id']
        # Now, update the actor
        update_data = {'age': 35}
        response = requests.patch(f'{BASE_URL}/actors/{actor_id}', headers=headers, data=json.dumps(update_data))
        self.assertEqual(response.status_code, 200)

    # 1.7 Test DELETE /movies success
    def test_delete_movie_success(self):
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        # First, create a movie to delete
        post_response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
        self.assertEqual(post_response.status_code, 201)
        movie_id = post_response.json()['movie']['id']

        # Now, delete the movie
        delete_response = requests.delete(f'{BASE_URL}/movies/{movie_id}', headers=headers)
        self.assertEqual(delete_response.status_code, 200)


    # 1.8 Test DELETE /actors success
    def test_delete_actor_success(self):
        """Test that an Executive Producer can successfully delete an actor."""
        
        # Set up headers with the correct authorization token
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }

        # First, create an actor to delete
        post_response = requests.post(f'{BASE_URL}/actors', headers=headers,  data=json.dumps(self.actor))
        
        # # Check if the POST request was successful
        # print(f"POST /actors status code: {post_response.status_code}")
        # print(f"POST /actors response content: {post_response.content}")
        
        # If the status code is not 201, something went wrong
        self.assertEqual(post_response.status_code, 201)
        
        # Parse the JSON response to get the actor ID
        actor_id = post_response.json()['actor']['id']
        
        # Now, delete the actor
        delete_response = requests.delete(f'{BASE_URL}/actors/{actor_id}', headers=headers)
        
        # # Check if the DELETE request was successful
        # print(f"DELETE /actors/{actor_id} status code: {delete_response.status_code}")
        # print(f"DELETE /actors/{actor_id} response content: {delete_response.content}")
        
        self.assertEqual(delete_response.status_code, 200)


# # ----------------------------------------
# # 2. Error Behavior Tests for Each Endpoint
# # ----------------------------------------

    # 2.1 Test GET /movies unauthorized
    def test_get_movies_unauthorized(self):
        """Test that accessing /movies without authorization returns 401."""
        headers = {}  # No Authorization header
        response = requests.get(f'{BASE_URL}/movies', headers=headers)
        self.assertEqual(response.status_code, 401)

    # 2.2 Test GET /actors unauthorized
    def test_get_actors_unauthorized(self):
        """Test that accessing /actors without authorization returns 401."""
        headers = {}  # No Authorization header
        response = requests.get(f'{BASE_URL}/actors', headers=headers)
        self.assertEqual(response.status_code, 401)

    # 2.3 Test POST /movies unprocessable
    def test_post_movie_unprocessable(self):
        """Test that creating a movie with incomplete data returns 422."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        incomplete_movie = {'title': 'Incomplete Movie'}  # Missing 'release_date'
        response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(incomplete_movie))
        self.assertEqual(response.status_code, 422)

    # 2.4 Test POST /actors unprocessable
    def test_post_actor_unprocessable(self):
        """Test that creating an actor with incomplete data returns 422."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        incomplete_actor = {'name': 'Incomplete Actor'}  # Missing 'age' and 'gender'
        response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(incomplete_actor))
        self.assertEqual(response.status_code, 422)

    # 2.5 Test PATCH /movies not found
    def test_patch_movie_not_found(self):
        """Test that updating a non-existent movie returns 404."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.patch(f'{BASE_URL}/movies/9999', headers=headers, data=json.dumps({'title': 'Does not exist'}))
        self.assertEqual(response.status_code, 404)

    # 2.6 Test PATCH /actors not found
    def test_patch_actor_not_found(self):
        """Test that updating a non-existent actor returns 404."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.patch(f'{BASE_URL}/actors/9999', headers=headers, data=json.dumps({'age': 100}))
        self.assertEqual(response.status_code, 404)

    # 2.7 Test DELETE /movies not found
    def test_delete_movie_not_found(self):
        """Test that deleting a non-existent movie returns 404."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}'
        }
        response = requests.delete(f'{BASE_URL}/movies/9999', headers=headers)
        self.assertEqual(response.status_code, 404)

    # 2.8 Test DELETE /actors not found
    def test_delete_actor_not_found(self):
        """Test that deleting a non-existent actor returns 404."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}'
        }
        response = requests.delete(f'{BASE_URL}/actors/9999', headers=headers)
        self.assertEqual(response.status_code, 404)

# # ----------------------------------------
# # 3. RBAC Tests for Each Role (At Least Two Tests per Role)
# # ----------------------------------------

    # 3.1 Casting Assistant Tests

    # 3.1.1 Test Casting Assistant can GET /movies
    def test_casting_assistant_get_movies(self):
        """Test that a Casting Assistant can access GET /movies."""
        headers = {
            'authorization': f'Bearer {ASSISTANT_TOKEN}'
        }
        response = requests.get(f'{BASE_URL}/movies', headers=headers)
        self.assertEqual(response.status_code, 200)

    # 3.1.2 Test Casting Assistant cannot DELETE /actors
    def test_casting_assistant_delete_actor_forbidden(self):
        """Test that a Casting Assistant cannot delete an actor."""
        headers = {
            'authorization': f'Bearer {ASSISTANT_TOKEN}'
        }
        response = requests.delete(f'{BASE_URL}/actors/1', headers=headers)
        self.assertEqual(response.status_code, 403)

    # 3.2 Casting Director Tests

    # 3.2.1 Test Casting Director can POST /actors
    def test_casting_director_add_actor(self):
        """Test that a Casting Director can add a new actor."""
        headers = {
            'authorization': f'Bearer {DIRECTOR_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))
        self.assertEqual(response.status_code, 201)

    # 3.2.2 Test Casting Director cannot DELETE /movies
    def test_casting_director_delete_movie_forbidden(self):
        """Test that a Casting Director cannot delete a movie."""
        headers = {
            'authorization': f'Bearer {DIRECTOR_TOKEN}'
        }
        response = requests.delete(f'{BASE_URL}/movies/1', headers=headers)
        self.assertEqual(response.status_code, 403)

    # 3.3 Executive Producer Tests

    # 3.3.1 Test Executive Producer can POST /movies
    def test_executive_producer_add_movie(self):
        """Test that an Executive Producer can add a new movie."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f'{BASE_URL}/movies', headers=headers, data=json.dumps(self.movie))
        self.assertEqual(response.status_code, 201)

    # 3.3.2 Test Executive Producer can DELETE /actors
    def test_executive_producer_delete_actor(self):
        """Test that an Executive Producer can delete an actor."""
        headers = {
            'authorization': f'Bearer {PRODUCER_TOKEN}',
            'Content-Type': 'application/json'
        }
        post_response = requests.post(f'{BASE_URL}/actors', headers=headers, data=json.dumps(self.actor))

        # Log the status code and content of the POST request for debugging
        print(f"POST /actors status code: {post_response.status_code}")
        print(f"POST /actors response content: {post_response.content}")

        # Ensure the POST request was successful before continuing
        self.assertEqual(post_response.status_code, 201)

        # Parse the JSON response to get the actor ID
        actor_id = post_response.json().get('actor', {}).get('id')

        # If actor_id is None, log an error
        if actor_id is None:
            print("Error: No actor ID returned in the response.")
        
        # Now, delete the actor
        response = requests.delete(f'{BASE_URL}/actors/{actor_id}', headers=headers)
        
        # Log the status code and content of the DELETE request for debugging
        print(f"DELETE /actors/{actor_id} status code: {response.status_code}")
        print(f"DELETE /actors/{actor_id} response content: {response.content}")

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
