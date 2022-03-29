import time
from ast import Param
from json import dumps, loads

# controler de serie
# controler de episodio
# model de episodio
# banco

# from db import db
from src.model.model_base import ModelBase


class SerieModel(ModelBase):
    __tablename__ = "series"
    __columns__ = ("id", "title", "resume", "genre", "rating", "season")

    id = None

    def build(self, title, resume, genre, rating, season, id=None):
        self.id = id
        self.title = title
        self.resume = resume
        self.genre = genre
        self.rating = rating
        self.season = season
        return self
