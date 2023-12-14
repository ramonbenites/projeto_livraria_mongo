from model.livro import Livro
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO
from model.categoria import Categoria
from model.editora import Editora
from model.autor import Autor
from database.client_factory import ClientFactory
from bson import ObjectId


class LivroDAO:

    def __init__(self, categoria_dao: CategoriaDAO, editora_dao: EditoraDAO, autor_dao: AutorDAO):
        self.__client = ClientFactory()
        self.__categoria_dao: CategoriaDAO = categoria_dao
        self.__editora_dao: EditoraDAO = editora_dao
        self.__autor_dao: AutorDAO = autor_dao

    def listar(self) -> list[Livro]:
        livros = list()

        client = self.__client.get_client()
        db = client.livraria
        for documento in db.livros.find():
            categoria: Categoria = self.__categoria_dao.buscar_por_id(
                documento['categoria_id'])
            editora: Editora = self.__editora_dao.buscar_por_id(
                documento['editora_id'])
            autor: Autor = self.__autor_dao.buscar_por_id(
                documento['autor_id'])

            liv = Livro(documento['titulo'], documento.get('resumo', ''), documento['ano'], documento['paginas'],
                        documento['isbn'], categoria, editora, autor)
            liv.id = documento['_id']

            livros.append(liv)
        client.close()

        return livros

    def adicionar(self, livro: Livro) -> None:
        client = self.__client.get_client()
        db = client.livraria
        db.livros.insert_one({'titulo': livro.titulo, 'resumo': livro.resumo, 'ano': livro.ano, 'paginas': livro.paginas,
                              'isbn': livro.isbn, 'categoria_id': livro.categoria.id,
                              'editora_id': livro.editora.id, 'autor_id': livro.autor.id})
        client.close()

    def remover(self, livro_id: ObjectId) -> bool:
        client = self.__client.get_client()
        db = client.livraria
        resultado = db.livros.delete_one({'_id': livro_id})
        if (resultado.deleted_count == 1):
            return True
        return False

    def buscar_por_id(self, livro_id: ObjectId) -> Livro:
        liv = None

        client = self.__client.get_client()
        db = client.livraria
        resultado = db.livros.find_one({'_id': livro_id})
        if (resultado):
            categoria: Categoria = self.__categoria_dao.buscar_por_id(
                resultado['categoria_id'])
            editora: Editora = self.__editora_dao.buscar_por_id(
                resultado['editora_id'])
            autor: Autor = self.__autor_dao.buscar_por_id(
                resultado['autor_id'])

            liv = Livro(resultado['titulo'], resultado.get('resumo', ''), resultado['ano'], resultado['paginas'],
                        resultado['isbn'], categoria, editora, autor)
            liv.id = resultado['_id']

        return liv
