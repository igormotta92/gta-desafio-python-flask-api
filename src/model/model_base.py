from dataclasses import field


class ModelBase:
    __tablename__ = None
    __columns__ = ()
    _db = None

    def __repr__(self) -> str:
        # print(repr(movie))
        aux = []
        for column in self.__columns__:
            aux.append(f"{column}={self.__dict__[column]}")

        filds = ", \r\n\t".join(aux)
        txt = f"{self.__class__} (\r\n\t{filds}\r\n)"

        return txt

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def to_dict(self):
        values = {}
        for column in self.__columns__:
            values[column] = self.__dict__[column]

        return values

    def insert(self):
        values = {}
        for column in self.__columns__:
            values[column] = self.__dict__[column]

        res = self._db.insert(self.__tablename__, values)
        return res

    def update(self):
        values = {}
        for column in self.__columns__:
            values[column] = self.__dict__[column]
        del values["id"]

        res = self._db.update(self.__tablename__, values, "id=?", [self.id])
        return res

    def delete(self):
        res = self._db.delete(self.__tablename__, "id=?", [self.id])
        return res

    @classmethod
    def setConnectDataBase(cls, value):
        cls._db = value

    @classmethod
    def find_all(cls):
        sql = f"SELECT * FROM {cls.__tablename__}"
        res = cls._db.pquey(sql).fetchall()
        return res

    @classmethod
    def find_by_id(cls, id):
        sql = f"SELECT * FROM {cls.__tablename__} WHERE id = ? "
        res = cls._db.pquey(sql, [id]).fetchone()

        return res

    @classmethod
    def find_by_id_build(cls, id):
        data = cls.find_by_id(id)

        if not data:
            return False

        movie = cls()
        for column in cls.__columns__:
            setattr(movie, column, data[column])

        return movie
