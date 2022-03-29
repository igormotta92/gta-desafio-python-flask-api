import time
from ast import Param
from json import dumps, loads

# from db import db
from src.model.model_base import ModelBase


class MovieModel(ModelBase):
    __tablename__ = "movies"
    __columns__ = ("id", "title", "resume", "genre", "rating", "year_release")

    id = None

    def build(self, title, resume, genre, rating, year_release, id=None):
        self.id = id
        self.title = title
        self.resume = resume
        self.genre = genre
        self.rating = rating
        self.year_release = year_release
        return self
