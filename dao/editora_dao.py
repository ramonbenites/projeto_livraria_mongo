from model.editora import Editora
from database.client_factory import ClientFactory
from bson import ObjectId


class EditoraDAO:

    def __init__(self):
        self.__client: ClientFactory = ClientFactory()

    def listar(self) -> list[Editora]:
        editoras = list()

        client = self.__client.get_client()
        db = client.livraria
        for documento in db.editoras.find():
            edt = Editora(
                documento['nome'], documento['endereco'], documento['telefone'])
            edt.id = documento['_id']
            editoras.append(edt)
        client.close()

        return editoras

    def adicionar(self, editora: Editora) -> None:
        client = self.__client.get_client()
        db = client.livraria
        db.editoras.insert_one(
            {'nome': editora.nome, 'endereco': editora.endereco, 'telefone': editora.telefone})
        client.close()

    def remover(self, editora_id: ObjectId) -> bool:
        client = self.__client.get_client()
        db = client.livraria
        resultado = db.editoras.delete_one({'_id': editora_id})
        if (resultado.deleted_count == 1):
            return True
        return False

    def buscar_por_id(self, editora_id: ObjectId) -> Editora:
        edt = None
        client = self.__client.get_client()
        db = client.livraria
        resultado = db.editoras.find_one({'_id': editora_id})
        if (resultado):
            edt = Editora(
                resultado['nome'], resultado['endereco'], resultado['telefone'])
            edt.id = resultado['_id']
        return edt
