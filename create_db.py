# __columns__ movie= ("id", "title", "resume", "genre", "rating", "year_release")
# __columns__ series = ("id", "title", "resume", "genre", "rating", "season")
# __columns__ episodes = ("id", "id_serie", "title", "resume", "season")


def sql_create_table_movies():
    return """
        CREATE TABLE IF NOT EXISTS movies (
            id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
            title text, 
            resume text, 
            genre text,
            rating integer,
            year_release integer
        );
        """


def sql_create_table_series():
    return """
        CREATE TABLE IF NOT EXISTS series (
            id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
            title text, 
            resume text, 
            genre text,
            rating integer,
            season integer
        );
        """


def sql_create_table_episodes():
    return """
        CREATE TABLE IF NOT EXISTS episodes (
            id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
            id_serie integer, 
            title text, 
            resume text, 
            season integer,
            episode_number integer,
            FOREIGN KEY(id_serie) REFERENCES series(id)
        );
        """
