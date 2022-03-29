# https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query

# from flask import Flask
from flask_restful import Resource, reqparse
from src.model.serie import SerieModel
from src.server.instance import server
from db import db

# books_db = [{"id": 0, "title": "War and Peace"}, {"id": 1, "title": "Clean Code"}]

api = server.api


class SeriesController(Resource):
    @classmethod
    def routes(self):
        api.add_resource(Series, "/series/<int:id>")
        api.add_resource(SeriesList, "/series")


class Series(Resource):
    def get(self, id):
        SerieModel.setConnectDataBase(db)
        serie = SerieModel.find_by_id(id)
        if not serie:
            return {serie}, 204

        return serie

    def put(self, id):
        SerieModel.setConnectDataBase(db)
        serie = SerieModel.find_by_id_build(id)
        if not serie:
            return None, 204

        #  __columns__ = ("title" str, "resume" str, "genre" str, "rating" int, "season" int)
        parser = reqparse.RequestParser()
        parser.add_argument(
            "title", type=str, required=True, help="Title cannot be blank"
        )
        parser.add_argument(
            "resume", type=str, required=True, help="Resume cannot be blank"
        )
        parser.add_argument(
            "rating",
            type=int,
            choices=range(1, 6),
            required=True,
            help="rating cannot be blank or range invalided",
        )
        parser.add_argument(
            "genre", type=str, required=True, help="Genre cannot be blank"
        )
        parser.add_argument(
            "season", type=int, required=True, help="Season cannot be blank"
        )
        data = parser.parse_args()

        # update
        serie.title = data.title
        serie.resume = data.resume
        serie.genre = data.genre
        serie.rating = data.rating
        serie.season = data.season
        try:
            serie.update()
        except Exception as error:
            return {"Error": str(error)}, 400

        return None, 200, {"Location": f"http://127.0.0.1:5000/series/{id}"}

    def delete(self, id):
        SerieModel.setConnectDataBase(db)
        serie = SerieModel.find_by_id_build(id)
        if not serie:
            return {}, 204

        serie.delete()
        return serie.to_dict(), 200


class SeriesList(Resource):
    def get(self):
        SerieModel.setConnectDataBase(db)
        try:
            series = SerieModel.find_all()
        except Exception as error:
            return {"Error": str(error)}, 400
        return series

    def post(self):
        SerieModel.setConnectDataBase(db)

        ###
        #  __columns__ = ("title" str, "resume" str, "genre" str, "rating" int, "season" int)
        # request
        parser = reqparse.RequestParser()
        parser.add_argument(
            "title", type=str, required=True, help="Title cannot be blank"
        )
        parser.add_argument(
            "resume", type=str, required=True, help="Resume cannot be blank"
        )
        parser.add_argument(
            "genre", type=str, required=True, help="Genre cannot be blank"
        )
        parser.add_argument(
            "rating",
            type=int,
            required=True,
            choices=range(1, 6),
            help="rating cannot be blank or range invalided",
        )
        parser.add_argument(
            "season", type=str, required=True, help="Season cannot be blank"
        )
        data = parser.parse_args()
        ###

        serie = SerieModel().build(
            data.title, data.resume, data.genre, data.rating, data.season
        )

        try:
            lastid = serie.insert().lastrowid
        except Exception as error:
            return {"Error": str(error)}, 400

        return None, 201, {"Location": f"http://127.0.0.1:5000/series/{lastid}"}
