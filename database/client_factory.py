from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_client(self):

    return MongoClient(
        'mongodb+srv://ramonbenites:Rsb03091031@cluster0.n5ezg1v.mongodb.net/?retryWrites=true&w=majority',
        server_api=ServerApi('1'))
