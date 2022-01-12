import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from werkzeug import test
from app import create_app
from models import setup_db, Actor, Movie, actorsinmovies
from mylog import mylog
from datetime import date, datetime
from dotenv import load_dotenv

# Tests are mainly route handler function tests and user role permissions test
# Function tests are done using Executive Producer token as that role has no permission limitation
load_dotenv()

class TestFamoso(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.environ.get("DB_NAME")
        self.host = os.environ.get("DB_HOST")
        self.user = os.environ.get("DB_USER")
        self.pw = os.environ.get("DB_PW")
        self.database_path = f"postgresql://{self.user}:{self.pw}@{self.host}/{self.database_name}"

        setup_db(self.app, self.database_path)

        self.casting_assistant_token = os.environ.get("TOKEN_CA")
        self.casting_director_token = os.environ.get("TOKEN_CD")
        self.executive_producer_token = os.environ.get("TOKEN_EP")

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

# ==================================
# Route handlers functionality tests
# ==================================
    # GET /actors success
    def test_EP_show_actors(self):
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().get("/actors", headers = header)
        data = json.loads(resp.data)
        mylog(data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["actors"])

    # GET /actors fail
    def test_EP_show_actors_page_error(self):
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().get("/actors?page=9999", headers = header)
        self.assertEqual(resp.status_code, 404)

    # POST /actor success
    def test_EP_add_new_actor(self):
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().post("/actors", headers = header, json = {
            "name": "Test Actor",
            "birthdate": "1984-01-24",
            "gender": "m"
        })

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)

        # Remove after test
        actor = Actor.query.filter(Actor.name=="Test Actor").one_or_none()
        actor.delete()

    # DELETE /actor success
    def test_EP_delete_actor(self):
        # Create the actor to test for deletetion
        bd = date(1984,1,24)
        stunt = Actor(name='Stunt Actor', birthdate=bd, gender='m')
        stunt.insert()

        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().delete("/actors/" + str(stunt.id), headers = header)

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)

    # PATCH /actor success
    def test_EP_edit_actor(self):
        # Create the actor to test for editing
        bd = date(1990,1,24)
        stunt = Actor(name='Patch Actor', birthdate=bd, gender='f')
        stunt.insert()

        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }
        resp = self.client().patch("/actors/" + str(stunt.id), headers = header, json = {
            "name": "Patched Actor",
            "birthdate": "1991-01-24",
            "gender": "m"
        })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        self.assertEqual(data["message"], f"Actor with ID: {stunt.id} has been patched")

        # Remove after test
        actor = Actor.query.filter(Actor.name=="Patched Actor").one_or_none()
        actor.delete()

    # GET /movies success
    def test_EP_show_movies(self):
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().get("/movies", headers = header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data["movies"])

    # GET /movies fail
    def test_EP_show_movies_page_error(self):
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().get("/movies?page=9999", headers = header)
        self.assertEqual(resp.status_code, 404)

    # POST /movie success
    def test_EP_add_new_movie(self):
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().post("/movies", headers = header, json = {
            "title": "Test Movie",
            "year": 2012
        })

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)

        # Remove after test
        movie = Movie.query.filter(Movie.title=="Test Movie").one_or_none()
        movie.delete()

    # DELETE /movie success
    def test_EP_delete_movie(self):
        # Create the movie to test for deletetion
        test = Movie(title='Audition Movie', year='2022')
        test.insert()

        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }

        resp = self.client().delete("/movies/" + str(test.id), headers = header)

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)

    # PATCH /movie success
    def test_EP_edit_movie(self):
        # Create the movie to test for deletetion
        test = Movie(title='Fake Movie', year=2022)
        test.insert()

        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }
        resp = self.client().patch("/movies/" + str(test.id), headers = header, json = {
            "title": "Freak Movie",
            "year": 2012
        })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        self.assertEqual(data["message"], f"Movie with ID: {test.id} has been patched")

        # Remove after test
        movie = Movie.query.filter(Movie.title=="Freak Movie").one_or_none()
        movie.delete()

    # GET movies of an actor/actors of a movie success
    def test_EP_get_movies_of_actor(self):
        # Set up actors and movies for test
        bd = date(1990,1,1)
        actor = Actor(name='Movie Actor', birthdate=bd, gender='f')
        actor.insert()
        movie = Movie(title='Actor Movie', year=2022)
        movie.actors.append(actor)
        movie.insert()

        # Call the route handler
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }
        resp = self.client().get("/movies/" + str(movie.id) + "/actors", headers = header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["starring"])

        # Clean up after test
        actorsinmovies.delete().where(actorsinmovies.c.actor_id==actor.id)
        movie.delete()
        actor.delete()

    # Associate actors and movies Does NOT work
    def test_EP_link_actor_movie(self):
        # Set up actors and movies for test
        bd = date(2000,1,1)
        actor = Actor(name='Link Actor', birthdate=bd, gender='f')
        actor.insert()
        movie = Movie(title='Link Movie', year=2022)
        movie.insert()

        # Call the route handler
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }
        resp = self.client().patch("/movies/" + str(movie.id) + "/" + str(actor.id), headers = header)
        data = json.loads(resp.data)

        movie = Movie.query.filter(Movie.title=="Link Movie").one_or_none()
        actor = Actor.query.filter(Actor.name=="Link Actor").one_or_none()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"], f"Actor {actor.id} is set to star in movie {movie.id}")

        # Clean up after test
        actorsinmovies.delete().where(actorsinmovies.c.actor_id==actor.id)
        movie.delete()
        actor.delete()

    # Break association between actor and movie
    def test_EP_break_link_actor_movie(self):
        # Set up actors and movies for test
        bd = date(1990,1,1)
        actor = Actor(name='Break Actor', birthdate=bd, gender='f')
        actor.insert()
        movie = Movie(title='Break Movie', year=2022)
        movie.actors.append(actor)
        movie.insert()

        # Call the route handler
        header = {
            "Authorization": f"Bearer {self.executive_producer_token}"
        }
        resp = self.client().delete("/movies/" + str(movie.id) + "/" + str(actor.id), headers = header)
        data = json.loads(resp.data)

        movie = Movie.query.filter(Movie.title=="Break Movie").one_or_none()
        actor = Actor.query.filter(Actor.name=="Break Actor").one_or_none()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"], f"Actor {actor.id} is removed from movie {movie.id}.")

        # Clean up after test
        actorsinmovies.delete().where(actorsinmovies.c.actor_id==actor.id)
        movie.delete()
        actor.delete()


# ===========
# RBAC Tests
# ===========
    def test_CA_view_movies_of_actor_success(self):
        header = {
            "Authorization": f"Bearer {self.casting_assistant_token}"
        }
        resp = self.client().get("actors/1/movies", headers = header)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["starring in"])


    def test_CA_post_movie_fail(self):
        header = {
            "Authorization": f"Bearer {self.casting_assistant_token}"
        }
        resp = self.client().post("/movies", headers = header, json = {
            "title": "Test Movie",
            "year": 2012
        })

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found")


    def test_CD_post_actor_success(self):
        header = {
            "Authorization": f"Bearer {self.casting_director_token}"
        }
        resp = self.client().post("/actors", headers = header, json = {
            "name": "TestCD Actor",
            "birthdate": "1984-01-24",
            "gender": "m"
        })

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)

        # Remove after test
        actor = Actor.query.filter(Actor.name=="TestCD Actor").one_or_none()
        actor.delete()


    def test_CD_post_movie_fail(self):
        header = {
            "Authorization": f"Bearer {self.casting_director_token}"
        }
        resp = self.client().post("/movies", headers = header, json = {
            "title": "TestCD Movie",
            "year": 2012
        })

        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found")

if __name__ == "__main__":
    unittest.main()