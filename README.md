# FaMoSo, a companion for an imaginary casting agency

## Introduction
This is the capstone project for Udacity Full Stack Developer ND program. It follows the "Casting Agency" specifications.

## URL
You can click on this link to go to live project page: insert link here!!!

## Authentication information

## Models
- Movies with title and release year
- Actors with name, birthdate and gender
- These two have a many-to-many relationship and it is represented by the actorsnmovies table (not a model itself)

## Endpoints
(Please use the postman collection to test the specific endpoints along with their auhorization tokens.)
- /actors
    - ['GET'] returns all actors as a json list (10 actors per page) along with a success message; requires the "view:actors" permission.
    - ['POST'] adds a new actor to the database; returns the name of added actor;requires "add:actor" permission.
    - ['DELETE'] deletes a single actor; accepts the id of the actor to be deleted; returns success upon deletion and echoes the id; requires "delete:actor" permission.
    - ['PATCH'] edits a single actor; accepts the id of the actor to be edited; if no input is given nothing happens even if it returns success; requires "edit:actor" permission
- /actors/<actor_id>/movies
    - ['GET'] returns all the movies for the actor defined by <actor_id>; requires "view:movies" permission. Same fuctionality is offered by the /movies/<movie_id>/actors endpoint.
- /movies
    - ['GET'] returns all movies as a json list (10 movies per page) along with a success message; requires the "view:movies" permission.
    - ['POST'] adds a new movie to the database; returns the title of added movie;requires "add:movie" permission.
    - ['DELETE'] deletes a single movie; accepts the id of the movie to be deleted; returns success upon deletion and echoes the id; requires "delete:movie" permission.
    - ['PATCH'] edits a single movie; accepts the id of the movie to be edited; if no input is given nothing happens even if it returns success; requires "edit:movie" permission
- /movies/<movie_id>/actors
    - ['GET'] returns all the actors for the movie defined by <movie_id>; requires "view:actors" permission. Same fuctionality is offered by the /actors/<actor_id>/movies endpoint.
-/movies/<movie_id>/<actor_id>
    - ['PATCH'] selects a movie and an actor already existing in the database and associates the two; requires "link:items" permission.
    - ['DELETE'] selects a movie and an actor and removes the association between the two if they have been previously associated in error; requires "link:items" permission.

## Roles
- _Casting Assistant:_ can view actors and movies (**permissions:** view:actors, view:movies)
- _Casting Director:_ can view actors and movies, can add actors to or delete them from database, can modify actors or movies. (**permissions:** view:actors, view:movies, add:actor, delete:actor, edit:actor, edit:movie)
- _Executive Producer:_ In addition to everything above, can add movies to or delete them from database, can create or break movie-actor associations. (**permissions:**  _all available permissions -see below section_)

## Permissions available
Below are all of the individual permissions available. They are fairly self explanatory.
- view:actors
- view:movies
- add:actor
- add:movie
- edit:actor
- edit:movie
- delete:actor
- delete:movie
- link:items

## For local deploys

### Clone the repo from github

### Virtual environment
cd into cloned project directory and create a virtual environment.
Local development was performed with a Python 3.7 venv. To build virtual environments with a Python version other than what is already on your system (e.g. the most recent - 3.10 at the time of writing) you can use:

```python -m virtualenv -p="<path_to_the_pyhthon.exe_for_the_specific_verision" venv```

Subsequently activate your virtual environment:
In gitbash: ```source venv\Scripts\activate```

### Requirements
Once the venv is activated, run ```pip install -r requirements.txt```

- instead of a setup.sh file, I use python-dotenv package to load my environment variables. This is done by specifying them in an .env file and then later calling the load_env() function of the package at the top.

### Database
For local deploys:
- Create a database called capstone: psql -U postgres (pw: sa)
    ```create database capstone;```
- while under the root directory of the project in your psql prompt:
    ```\i capstone.sql```
    This will populate the database which is needed for at least one of the tests

### Launch the app
```export FLASK_APP=app.py``` and then ```flask run```

