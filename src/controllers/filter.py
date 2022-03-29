# https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query

# from flask import Flask
from flask import request
from flask_restful import Resource, reqparse
from src.model.serie import SerieModel
from src.server.instance import server
from db import db

# books_db = [{"id": 0, "title": "War and Peace"}, {"id": 1, "title": "Clean Code"}]

api = server.api


class FiltersController(Resource):
    @classmethod
    def routes(self):
        api.add_resource(Filters, "/filters")


# __columns__ movie= ("id", "title", "resume", "genre", "rating")
# __columns__ series = ("id", "title", "resume", "genre", "rating")


class Filters(Resource):
    def get(self):
        qs = request.args
        title = qs.get("title")

        args = []
        if title:
            args.append(f"%{title}%")

        sql = """
            SELECT * FROM (
                SELECT 
                    'movie' tipo,
                    id, 
                    title, 
                    resume, 
                    genre, 
                    rating
                FROM movies
                UNION ALL
                SELECT 
                    'series' tipo,
                    id, 
                    title, 
                    resume, 
                    genre, 
                    rating
                FROM series
            ) A
            WHERE title like ?
        """

        res = db.pquey(sql, args)
        # print(args)
        return res.fetchall()
