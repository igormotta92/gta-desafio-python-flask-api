# from flask import Flask
from flask_restful import Resource, reqparse
from src.model.episode import EpisodesModel
from src.model.serie import SerieModel
from src.server.instance import server
from db import db

api = server.api


class EpisodesController(Resource):
    @classmethod
    def routes(self):
        api.add_resource(Episodes, "/episodes/<int:id>")
        api.add_resource(EpisodesList, "/episodes")


class Episodes(Resource):
    def get(self, id):
        EpisodesModel.setConnectDataBase(db)
        episode = EpisodesModel.find_by_id(id)
        if not episode:
            return {}, 204

        return episode

    def put(self, id):
        EpisodesModel.setConnectDataBase(db)
        episode = EpisodesModel.find_by_id_build(id)
        if not episode:
            return None, 204

        parser = reqparse.RequestParser()
        parser.add_argument(
            "id_serie", type=int, required=True, help="Serie cannot be blank"
        )
        parser.add_argument(
            "title", type=str, required=True, help="Title cannot be blank"
        )
        parser.add_argument(
            "resume", type=str, required=True, help="Resume cannot be blank"
        )
        parser.add_argument(
            "season", type=int, required=True, help="Season cannot be blank"
        )
        parser.add_argument(
            "episode_number",
            type=int,
            required=True,
            help="Episode number cannot be blank",
        )
        data = parser.parse_args()

        episode.id_serie = data.id_serie
        episode.title = data.title
        episode.resume = data.resume
        episode.season = data.season
        episode.episode_number = data.episode_number

        try:
            episode.update()
        except Exception as error:
            return {"Error": str(error)}, 400

        return None, 200, {"Location": f"http://127.0.0.1:5000/episodes/{id}"}

    def delete(self, id):
        EpisodesModel.setConnectDataBase(db)
        episode = EpisodesModel.find_by_id_build(id)
        if not episode:
            return {}, 204

        episode.delete()
        return episode.to_dict(), 200


class EpisodesList(Resource):
    def get(self):
        EpisodesModel.setConnectDataBase(db)

        try:
            episodes = EpisodesModel.find_all()
        except Exception as error:
            return {"Error": str(error)}, 400
        return episodes

    def post(self):
        EpisodesModel.setConnectDataBase(db)
        SerieModel.setConnectDataBase(db)

        parser = reqparse.RequestParser()
        parser.add_argument(
            "id_serie", type=int, required=True, help="Serie cannot be blank"
        )
        parser.add_argument(
            "title", type=str, required=True, help="Title cannot be blank"
        )
        parser.add_argument(
            "resume", type=str, required=True, help="Resume cannot be blank"
        )
        parser.add_argument(
            "season", type=int, required=True, help="Season cannot be blank"
        )
        parser.add_argument(
            "episode_number",
            type=int,
            required=True,
            help="Episode number cannot be blank",
        )
        data = parser.parse_args()

        serie = SerieModel.find_by_id_build(data.id_serie)
        if not serie:
            return {"Error": "Serie not found"}, 400

        episode = EpisodesModel().build(
            data.id_serie, data.title, data.resume, data.season, data.episode_number
        )
        try:
            lastid = episode.insert().lastrowid
        except Exception as error:
            return {"Error": str(error)}, 400

        return None, 201, {"Location": f"http://127.0.0.1:5000/episodes/{lastid}"}
