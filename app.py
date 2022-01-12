import json
from flask import Flask, jsonify, abort, request
from models import setup_db, Actor, Movie, actorsinmovies
from sqlalchemy.orm.query import Query
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from auth import AuthError400, AuthError401, AuthError403, requires_auth
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # =================
    # Helper functions
    # =================
    def validate(date_text):
            try:
                return datetime.strptime(date_text, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Check the birthdate, should be YYYY-MM-DD")


    # ===============
    # Route handlers
    # ===============
    @app.route("/")
    def home():
        return jsonify({
            "success": True,
            "message": "Welcome to FaMoso, the casting agent companion. Please sign in."
        })

    @app.route("/callback")
    def callback():
        return jsonify({
            "message": "You have logged in to FaMoSo via Auth0!"
        })

    # Show all actors in a list
    @app.route("/actors", methods=['GET'])
    @requires_auth('view:actors')
    def show_actors(jwt):
        try:
            selection = Actor.query.order_by(Actor.id).paginate(
                per_page=10, page=request.args.get("page", 1, type=int)
            )

            actors_list = [
                actor.format() for actor in selection.items
            ]

            return jsonify({
                "success": True,
                "actors": actors_list,
                "total_actors": selection.total
            })
        except Exception:
            abort(404)


    # Add new actor
    @app.route("/actors", methods=['POST'])
    @requires_auth('add:actor')
    def post_actor(jwt):
        try:
            body = request.get_json()
            new_actor_name = body.get("name", None)
            new_actor_birthdate = body.get("birthdate", None)
            new_actor_gender = body.get("gender", None)
            check = [bool(new_actor_name), bool(new_actor_birthdate), bool(new_actor_gender)]


            if not all(check):
                abort(422)

            actor = Actor(name=new_actor_name, birthdate=validate(new_actor_birthdate), gender=new_actor_gender)
            actor.insert()

            return jsonify({
                "success": True,
                "message": f"Actor {new_actor_name} has been inserted!"
            })
        except Exception:
            abort(422)


    # Edit single actor
    @app.route("/actors/<int:actor_id>", methods=['PATCH'])
    @requires_auth('edit:actor')
    def edit_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                return jsonify({
                    "success": False,
                    "message": f"The actor (ID: {actor_id}) you are trying to edit does not exist"
                })

            body = request.get_json()
            new_actor_name = body.get("name", None)
            new_actor_birthdate = body.get("birthdate", None)
            new_actor_gender = body.get("gender", None)
            check = [bool(new_actor_name), bool(new_actor_birthdate), bool(new_actor_gender)]

            if not any(check):
                return jsonify({
                    "success": True,
                    "message": f"No changes were made to the actor with ID: {actor_id}"
                })

            if new_actor_name:
                actor.name = new_actor_name
            elif new_actor_birthdate:
                actor.birthdate = validate(new_actor_birthdate)
            elif new_actor_gender:
                actor.gender = new_actor_gender

            actor.update()

            return jsonify({
                "success": True,
                "message": f"Actor with ID: {actor_id} has been patched",
                "actor": actor.format()
            })

        except Exception:
            return(404)


    # Delete single actor
    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                return jsonify({
                    "success": False,
                    "message": "The actor you are trying to delete does not exist"
                })
            actor.delete()

            return jsonify({
                "success": True,
                "deleted": actor_id
            })
        except Exception:
            abort(404)


    # Show all movies in a list
    @app.route("/movies", methods=['GET'])
    @requires_auth('view:movies')
    def show_movies(jwt):
        try:
            selection = Movie.query.order_by(Movie.id).paginate(
                per_page=10, page=request.args.get("page", 1, type=int)
            )

            movies_list = [
                movie.format() for movie in selection.items
            ]

            return jsonify({
                "success": True,
                "movies": movies_list,
                "total_movies": selection.total
            })
        except Exception:
            abort(404)


    # Add new movie
    @app.route("/movies", methods=['POST'])
    @requires_auth('add:movie')
    def post_movie(jwt):
        try:
            body = request.get_json()
            new_title = body.get("title", None)
            new_release_year = body.get("year", None)
            check = [bool(new_title), bool(new_release_year)]

            if not all(check):
                abort(422)

            movie = Movie(title=new_title, year=new_release_year)
            movie.insert()

            return jsonify({
                "success": True,
                "message": f"Movie {new_title} has been inserted!"
            })
        except Exception:
            abort(422)


    # Edit single movie
    @app.route("/movies/<int:movie_id>", methods=['PATCH'])
    @requires_auth('edit:movie')
    def edit_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                return jsonify({
                    "success": False,
                    "message": f"The movie (ID: {movie_id}) you are trying to edit does not exist"
                })

            body = request.get_json()
            new_title = body.get("title", None)
            new_relase_year = body.get("year", None)
            check = [bool(new_title), bool(new_relase_year)]

            if not any(check):
                return jsonify({
                    "success": True,
                    "message": f"No changes were made to the movie with ID: {movie_id}"
                })

            if new_title:
                movie.title = new_title
            elif new_relase_year:
                movie.year = new_relase_year

            movie.update()

            return jsonify({
                "success": True,
                "message": f"Movie with ID: {movie_id} has been patched",
                "movie": movie.format()
            })

        except Exception:
            return(404)


    # Delete single movie
    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                return jsonify({
                    "success": False,
                    "message": "The movie you are trying to delete does not exist"
                })
            movie.delete()

            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except Exception:
            abort(404)


    # Movies of an actor
    @app.route("/actors/<int:actor_id>/movies", methods=['GET'])
    @requires_auth('view:movies')
    def filmography(jwt, actor_id):
        try:
            movies = Movie.query.join(Actor, Movie.actors).filter(Actor.id==actor_id).all()
            formatted_list = [movie.format() for movie in movies]

            return jsonify({
                "success": True,
                "starring in": formatted_list
            })
        except Exception:
            abort(404)

    # Actors of a movie
    @app.route("/movies/<int:movie_id>/actors", methods=['GET'])
    @requires_auth('view:actors')
    def starring(jwt, movie_id):
        try:
            actors = Actor.query.join(Movie.actors).filter(Movie.id==movie_id).all()
            formatted_list = [actor.format() for actor in actors]

            return jsonify({
                "success": True,
                "starring": formatted_list
            })
        except Exception:
            abort(404)


    # Add actor-movie association
    @app.route("/movies/<int:movie_id>/<int:actor_id>", methods=['PATCH'])
    @requires_auth('link:items')
    def add_actor_to_movie(jwt, movie_id, actor_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            movie.actors.append(actor)
            movie.update()

            return jsonify({
                "success": True,
                "message": f"Actor {actor_id} is set to star in movie {movie_id}"
            })
        except Exception:
            abort(404)

    # Break actor-movie association
    @app.route("/movies/<int:movie_id>/<int:actor_id>", methods=['DELETE'])
    @requires_auth('link:items')
    def remove_actor_from_movie(jwt, movie_id, actor_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            movie.actors.remove(actor)
            movie.update()

            return jsonify({
                "success": True,
                "message": f"Actor {actor_id} is removed from movie {movie_id}."
            })
        except Exception:
            abort(404)

    # ===============
    # Auth  error handlers
    # ===============
    @app.errorhandler(AuthError400)
    def auth_error_400(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), 400


    @app.errorhandler(AuthError401)
    def auth_error_401(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), 401

    @app.errorhandler(AuthError403)
    def auth_error_403(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), 403

    # ==================
    # Other error handlers
    # =================
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
        )


    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
        )


    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
        )


    @app.errorhandler(500)
    def server_error(error):
        return (jsonify({
            "success": False,
            "error": 500,
            "message": "something went wrong on the server"
        }), 500
        )

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
