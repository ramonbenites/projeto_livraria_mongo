from bson import ObjectId


class Categoria:

    def __init__(self, nome: str):
        self.__id: ObjectId = None
        self.__nome: str = nome

    @property
    def id(self) -> ObjectId:
        return self.__id

    @id.setter
    def id(self, id: ObjectId):
        self.__id = id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
