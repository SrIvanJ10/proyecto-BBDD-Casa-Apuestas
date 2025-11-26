from pymongo import MongoClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBManager:
    _client = None
    _db = None
    
    @classmethod
    def get_db(cls):
        if cls._db is None:
            try:
                cls._client = MongoClient(
                    settings.MONGODB_URI,
                    maxPoolSize=50,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000
                )
                cls._db = cls._client[settings.MONGODB_DB_NAME]
                logger.info("Conexión a MongoDB establecida correctamente")
            except Exception as e:
                logger.error(f"Error conectando a MongoDB: {e}")
                raise
        return cls._db
    
    @classmethod
    def close_connection(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("Conexión a MongoDB cerrada")

def get_mongodb_collection(collection_name):
    """Obtener una colección de MongoDB"""
    db = MongoDBManager.get_db()
    return db[collection_name]