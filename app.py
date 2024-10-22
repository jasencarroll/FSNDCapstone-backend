import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Auth0 and RBAC imports
from auth import requires_auth

migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate.init_app(app, db)
    
    # GET /
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'success': True,
        }), 200

    # GET /movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': formatted_movies
        }), 200

    # GET /actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200

    # POST /movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title or not release_date:
            abort(422)

        try:
            # Create a new movie object
            movie = Movie(title=title, release_date=release_date)
            
            # Add and commit the movie to the database
            db.session.add(movie)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201
        except Exception as e:
            print(f"Error creating movie: {e}")
            db.session.rollback()  # Rollback in case of any errors
            abort(500)
        finally:
            db.session.close()  # Ensure the session is closed

    # POST /actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if not name or not age or not gender:
            abort(422)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            db.session.add(actor)
            db.session.commit()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except Exception as e:
            print(f"Error creating actor: {e}")
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    # DELETE /movies/<int:movie_id>
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        try:
            db.session.delete(movie)
            db.session.commit()
            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200
        except Exception as e:
            print(f"Error deleting movie: {e}")
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    # DELETE /actors/<int:actor_id>
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        try:
            db.session.delete(actor)
            db.session.commit()
            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200
        except Exception as e:
            print(f"Error deleting actor: {e}")
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    # PATCH /movies/<int:movie_id>
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date

        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except Exception as e:
            print(f"Error updating movie: {e}")
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    # PATCH /actors/<int:actor_id>
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender

        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except Exception as e:
            print(f"Error updating actor: {e}")
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
