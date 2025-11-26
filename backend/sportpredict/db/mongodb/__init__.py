from .partidos import PartidoStatsManager
from .analytics import AnalyticsManager
from .conexion import MongoDBManager

# Exportar instancia de la base de datos
mongo_db = MongoDBManager.get_db()

__all__ = ['PartidoStatsManager', 'AnalyticsManager', 'mongo_db', 'MongoDBManager']