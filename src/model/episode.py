import time
from ast import Param
from json import dumps, loads

# from db import db
from src.model.model_base import ModelBase


class EpisodesModel(ModelBase):
    __tablename__ = "episodes"
    __columns__ = ("id", "id_serie", "title", "resume", "season", "episode_number")

    id = None

    def build(self, id_serie, title, resume, season, episode_number, id=None):
        self.id = id
        self.id_serie = id_serie
        self.title = title
        self.resume = resume
        self.season = season
        self.episode_number = episode_number
        return self
