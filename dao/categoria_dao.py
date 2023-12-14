from model.categoria import Categoria
from database.client_factory import ClientFactory
from bson import ObjectId


class CategoriaDAO:

    def __init__(self):
        self.__client: ClientFactory = ClientFactory()

    def listar(self) -> list[Categoria]:
        categorias = list()

        client = self.__client.get_client()
        db = client.livraria
        for documento in db.categorias.find():
            cat = Categoria(documento['nome'])
            cat.id = documento['_id']
            categorias.append(cat)
        client.close()

        return categorias

    def adicionar(self, categoria: Categoria) -> None:
        client = self.__client.get_client()
        db = client.livraria
        db.categorias.insert_one({'nome': categoria.nome})
        client.close()

    def remover(self, categoria_id: ObjectId) -> bool:
        client = self.__client.get_client()
        db = client.livraria
        resultado = db.categorias.delete_one({'_id': categoria_id})
        client.close()
        if (resultado.deleted_count == 1):
            return True
        return False

    def buscar_por_id(self, categoria_id: ObjectId) -> Categoria:
        cat = None
        client = self.__client.get_client()
        db = client.livraria
        resultado = db.categorias.find_one({'_id': categoria_id})
        client.close()
        if (resultado):
            cat = Categoria(resultado['nome'])
            cat.id = resultado['_id']
        return cat
