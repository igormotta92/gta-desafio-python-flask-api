import sqlite3
from sqlite3 import Error
from create_db import *


class db_sqlite3:
    def __init__(self) -> None:
        self._db_connection = sqlite3.connect("movies.db", check_same_thread=False)
        # self._db_connection.row_factory = sqlite3.Row
        self._db_connection.row_factory = self.dict_factory
        self._cursor = self._db_connection.cursor()

    # Convert query result in dictionary
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __del__(self) -> None:
        self._db_connection.close()

    def commit(self):
        self._db_connection.commit()

    def pquey(self, sql, args=[]):
        self._res = self._cursor.execute(sql, args)
        return self._res

    def pquey_commit(self, sql, args=[]):
        res = self.pquey(sql, args)
        self._db_connection.commit()
        return res

    def insert(self, table, values):
        fields = []
        parms_bind = []
        args = []
        for field, value in values.items():
            fields.append(field)
            parms_bind.append("?")
            args.append(value)

        # ','.join(str(v) for v in fields)
        fields_insert = ", ".join(fields)
        binds_insert = ", ".join(parms_bind)

        sql = f"""
            INSERT INTO {table} ({fields_insert})
            VALUES ({binds_insert})
        """
        res = self.pquey_commit(sql, args)

        return res

    def update(self, table, values, where, args=[]):
        fields = []
        args_values = []
        for field, value in values.items():
            fields.append(f"{field} = ?")
            args_values.append(value)

        fields_insert = ", ".join(fields)
        args = args_values + args

        sql = f"""
            UPDATE {table} SET {fields_insert}
            WHERE 1=1 AND {where}
        """

        res = self.pquey_commit(sql, args)
        return res

    def delete(self, table, where, args=[]):
        sql = f"""
            DELETE FROM {table}
            WHERE 1=1 AND {where}
        """

        res = self.pquey_commit(sql, args)

        return res

    ##################################################
    # migrations - create data base
    def create_all(self) -> None:
        slqs = [
            sql_create_table_movies(),
            sql_create_table_series(),
            sql_create_table_episodes(),
        ]

        try:
            for slq in slqs:
                self._cursor.execute(slq)
            self._db_connection.commit()
        except Error as ex:
            print(ex)


db = db_sqlite3()
