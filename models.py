import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from math import floor
from dotenv import load_dotenv

load_dotenv()
name = os.environ.get("HEROKU_DB_NAME")
host = os.environ.get("HEROKU_HOST")
user = os.environ.get("HEROKU_USER")
pw = os.environ.get("HEROKU_PW")
path = f"postgresql://{user}:{pw}@{host}/{name}"
db = SQLAlchemy()

def setup_db(app, database_path=path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

# Models
actorsinmovies = db.Table('actorsinmovies',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)

class Movie(db.Model):
    __tablename__ = "movie"
    __table_args__ = (db.UniqueConstraint('title', 'year'), )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    actors = db.relationship('Actor', secondary=actorsinmovies, lazy='dynamic', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f'<ID: {self.id}, Title: {self.title}>'

    def format(self):
        return{
            "id": self.id,
            "title": self.title,
            "year": self.year
            # "actors": self.actors
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = "actor"
    __table_args__ = (db.UniqueConstraint('name', 'birthdate'), )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String(1))

    def __repr__(self):
        return f'<{self.id}, {self.name}, {self.age()}, {self.gender}>'

    def format(self):
        return{
            "id": self.id,
            "name": self.name,
            "age": self.age(),
            "gender": self.gender
        }

    def age(self):
        daydelta = date.today() - self.birthdate
        return floor(daydelta.days / 365.25)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
