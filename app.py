from src.controllers.filter import FiltersController
from src.server.instance import server
from db import db
from src.controllers.movie import MoviesController
from src.controllers.serie import SeriesController
from src.controllers.episode import EpisodesController

app = server.app


@app.before_first_request
def create_table():
    db.create_all()


MoviesController.routes()
SeriesController.routes()
EpisodesController.routes()
FiltersController.routes()

if __name__ == "__main__":
    server.run()
