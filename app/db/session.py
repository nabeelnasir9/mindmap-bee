import certifi
from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.DATABASE_URL, tlsCAFile=certifi.where())
db = client.notes_app


def get_db():
    return db
