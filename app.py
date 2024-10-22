import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from flask_cors import CORS
from flask_migrate import Migrate
from models import db

# Auth0 and RBAC imports
from auth import requires_auth

migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate.init_app(app, db)

    # GET /movies
    @app.route('/movies', methods=['GET'])
    #@requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': formatted_movies
        }), 200

    # GET /actors
    @app.route('/actors', methods=['GET'])
    #@requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200

    # POST /movies
    @app.route('/movies', methods=['POST'])
    #@requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title or not release_date:
            abort(422)

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201
        except:
            abort(500)

    # POST /actors
    @app.route('/actors', methods=['POST'])
    #@requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if not name or not age or not gender:
            abort(422)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except:
            abort(500)

    # DELETE /movies/<int:movie_id>
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    #@requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        try:
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200
        except:
            abort(500)

    # DELETE /actors/<int:actor_id>
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    #@requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200
        except:
            abort(500)

    # PATCH /movies/<int:movie_id>
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    #@requires_auth('patch:movies')
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
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except:
            abort(500)

    # PATCH /actors/<int:actor_id>
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    #@requires_auth('patch:actors')
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
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except:
            abort(500)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
