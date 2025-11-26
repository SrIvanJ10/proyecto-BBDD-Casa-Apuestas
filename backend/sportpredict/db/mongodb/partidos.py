from .conexion import get_mongodb_collection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PartidoStatsManager:
    def __init__(self):
        self.collection = get_mongodb_collection('partido_stats')
    
    def guardar_estadisticas_futbol(self, partido_id, estadisticas):
        """Guardar estadísticas de un partido de fútbol"""
        try:
            document = {
                'partido_id': str(partido_id),
                'deporte': 'fútbol',
                'estadisticas_futbol': estadisticas,
                'timestamp': datetime.utcnow(),
                'actualizado_en': datetime.utcnow()
            }
            
            result = self.collection.update_one(
                {'partido_id': str(partido_id)},
                {'$set': document},
                upsert=True
            )
            
            logger.info(f"Estadísticas fútbol guardadas para partido {partido_id}")
            return result.upserted_id or True
            
        except Exception as e:
            logger.error(f"Error guardando estadísticas fútbol: {e}")
            return False
    
    def guardar_estadisticas_baloncesto(self, partido_id, estadisticas):
        """Guardar estadísticas de un partido de baloncesto"""
        try:
            document = {
                'partido_id': str(partido_id),
                'deporte': 'baloncesto',
                'estadisticas_baloncesto': estadisticas,
                'timestamp': datetime.utcnow(),
                'actualizado_en': datetime.utcnow()
            }
            
            result = self.collection.update_one(
                {'partido_id': str(partido_id)},
                {'$set': document},
                upsert=True
            )
            
            logger.info(f"Estadísticas baloncesto guardadas para partido {partido_id}")
            return result.upserted_id or True
            
        except Exception as e:
            logger.error(f"Error guardando estadísticas baloncesto: {e}")
            return False
    
    def obtener_estadisticas_partido(self, partido_id):
        """Obtener estadísticas de un partido específico"""
        try:
            document = self.collection.find_one(
                {'partido_id': str(partido_id)},
                {'_id': 0}  # Excluir el _id de MongoDB
            )
            return document
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas partido {partido_id}: {e}")
            return None
    
    def obtener_estadisticas_por_deporte(self, deporte):
        """Obtener todas las estadísticas de un deporte específico"""
        try:
            cursor = self.collection.find(
                {'deporte': deporte},
                {'_id': 0}
            )
            return list(cursor)
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas para {deporte}: {e}")
            return []
    
    def actualizar_mvp(self, partido_id, mvp_data, deporte):
        """Actualizar MVP para cualquier deporte"""
        try:
            campo_estadisticas = f'estadisticas_{deporte}'
            
            result = self.collection.update_one(
                {'partido_id': str(partido_id)},
                {
                    '$set': {
                        f'{campo_estadisticas}.mvp': mvp_data,
                        'actualizado_en': datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error actualizando MVP partido {partido_id}: {e}")
            return False