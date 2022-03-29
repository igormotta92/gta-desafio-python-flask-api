# https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query

# from flask import Flask
from flask_restful import Resource, reqparse
from src.model.movie import MovieModel
from src.server.instance import server
from db import db

# books_db = [{"id": 0, "title": "War and Peace"}, {"id": 1, "title": "Clean Code"}]
# ("id", "title", "resume", "genre", "rating", "year_release")
api = server.api


class MoviesController(Resource):
    @classmethod
    def routes(self):
        api.add_resource(Movies, "/movies/<int:id>")
        api.add_resource(MoviesList, "/movies")


class Movies(Resource):
    def get(self, id):
        MovieModel.setConnectDataBase(db)
        movie = MovieModel.find_by_id(id)
        if not movie:
            return {}, 204

        return movie

    def put(self, id):
        MovieModel.setConnectDataBase(db)
        movie = MovieModel.find_by_id_build(id)
        if not movie:
            return None, 204

        ###
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
            choices=range(1, 6),
            required=True,
            help="rating cannot be blank or range invalided",
        )
        parser.add_argument(
            "year_release", type=int, required=True, help="Year release cannot be blank"
        )
        data = parser.parse_args()
        ###

        # update
        movie.title = data.title
        movie.resume = data.resume
        movie.genre = data.genre
        movie.rating = data.rating
        movie.year_release = data.year_release

        try:
            movie.update()
        except Exception as error:
            return {"Error": str(error)}, 400

        return None, 200, {"Location": f"http://127.0.0.1:5000/movies/{id}"}

    def delete(self, id):
        MovieModel.setConnectDataBase(db)
        movie = MovieModel.find_by_id_build(id)
        if not movie:
            return {}, 204

        movie.delete()
        return movie.to_dict(), 200


class MoviesList(Resource):
    def get(self):
        MovieModel.setConnectDataBase(db)
        try:
            movies = MovieModel.find_all()
        except Exception as error:
            return {"Error": str(error)}, 400
        return movies

    def post(self):
        MovieModel.setConnectDataBase(db)

        ###
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
            choices=range(1, 6),
            required=True,
            help="rating cannot be blank or range invalided",
        )
        parser.add_argument(
            "year_release",
            type=int,
            required=True,
            help="Year realease cannot be blank",
        )
        data = parser.parse_args()
        ###

        movie = MovieModel().build(
            data.title, data.resume, data.genre, data.rating, data.year_release
        )
        try:
            lastid = movie.insert().lastrowid
        except Exception as error:
            return {"Error": str(error)}, 400

        return None, 201, {"Location": f"http://127.0.0.1:5000/movies/{lastid}"}
