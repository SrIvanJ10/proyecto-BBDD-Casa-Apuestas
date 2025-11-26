from .conexion import get_mongodb_collection
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AnalyticsManager:
    def __init__(self):
        self.stats_collection = get_mongodb_collection('partido_stats')
        self.dashboard_collection = get_mongodb_collection('analytics_dashboard')
        self.activity_collection = get_mongodb_collection('user_activity_logs')
    
    # MÉTODOS EXISTENTES (para partidos)
    def obtener_promedios_deporte(self, deporte):
        """Obtener promedios de estadísticas por deporte"""
        pipeline = [
            {'$match': {'deporte': deporte}},
            {'$group': {
                '_id': '$deporte',
                'total_partidos': {'$sum': 1},
                **self._get_avg_pipeline(deporte)
            }}
        ]
        
        try:
            result = list(self.stats_collection.aggregate(pipeline))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error en agregación: {e}")
            return None
    
    def _get_avg_pipeline(self, deporte):
        """Pipeline de promedios según el deporte"""
        if deporte == 'fútbol':
            return {
                'avg_goles_local': {'$avg': '$estadisticas_futbol.goles_local'},
                'avg_goles_visitante': {'$avg': '$estadisticas_futbol.goles_visitante'},
                'avg_posesion_local': {'$avg': '$estadisticas_futbol.posesion_local'},
                'avg_tiros_local': {'$avg': '$estadisticas_futbol.tiros_local'},
            }
        else:  # baloncesto
            return {
                'avg_puntos_local': {'$avg': '$estadisticas_baloncesto.puntos_local'},
                'avg_puntos_visitante': {'$avg': '$estadisticas_baloncesto.puntos_visitante'},
                'avg_rebotes_local': {'$avg': '$estadisticas_baloncesto.rebotes_local'},
                'avg_triples_local': {'$avg': '$estadisticas_baloncesto.triples_local'},
            }
    
    def obtener_partidos_recientes(self, dias=7):
        """Obtener partidos de los últimos N días"""
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        
        cursor = self.stats_collection.find(
            {'timestamp': {'$gte': fecha_limite}},
            {'_id': 0}
        ).sort('timestamp', -1)
        
        return list(cursor)
    
    # NUEVOS MÉTODOS PARA DASHBOARD Y ACTIVIDAD
    
    def guardar_metricas_dashboard(self, metricas):
        """Guardar métricas del dashboard para el día actual"""
        try:
            fecha_hoy = datetime.utcnow().strftime('%Y-%m-%d')
            
            document = {
                'date': fecha_hoy,
                'timestamp': datetime.utcnow(),
                **metricas
            }
            
            result = self.dashboard_collection.update_one(
                {'date': fecha_hoy},
                {'$set': document},
                upsert=True
            )
            
            logger.info(f"Métricas dashboard guardadas para {fecha_hoy}")
            return result.upserted_id or True
            
        except Exception as e:
            logger.error(f"Error guardando métricas dashboard: {e}")
            return False
    
    def obtener_metricas_dashboard(self, fecha=None):
        """Obtener métricas del dashboard para una fecha específica"""
        try:
            fecha_consulta = fecha or datetime.utcnow().strftime('%Y-%m-%d')
            
            document = self.dashboard_collection.find_one(
                {'date': fecha_consulta},
                {'_id': 0, 'timestamp': 0}
            )
            
            return document
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas dashboard: {e}")
            return None
    
    def obtener_historico_dashboard(self, dias=30):
        """Obtener histórico de métricas de los últimos N días"""
        try:
            fecha_limite = (datetime.utcnow() - timedelta(days=dias)).strftime('%Y-%m-%d')
            
            cursor = self.dashboard_collection.find(
                {'date': {'$gte': fecha_limite}},
                {'_id': 0}
            ).sort('date', 1)
            
            return list(cursor)
            
        except Exception as e:
            logger.error(f"Error obteniendo histórico dashboard: {e}")
            return []
    
    def registrar_actividad_usuario(self, user_id, action, metadata=None):
        """Registrar actividad de usuario"""
        try:
            document = {
                'user_id': str(user_id),
                'action': action,
                'timestamp': datetime.utcnow(),
                'metadata': metadata or {}
            }
            
            result = self.activity_collection.insert_one(document)
            logger.info(f"Actividad registrada para usuario {user_id}: {action}")
            return result.inserted_id
            
        except Exception as e:
            logger.error(f"Error registrando actividad usuario: {e}")
            return None
    
    def obtener_actividad_usuario(self, user_id, limite=50):
        """Obtener actividad reciente de un usuario"""
        try:
            cursor = self.activity_collection.find(
                {'user_id': str(user_id)},
                {'_id': 0}
            ).sort('timestamp', -1).limit(limite)
            
            return list(cursor)
            
        except Exception as e:
            logger.error(f"Error obteniendo actividad usuario {user_id}: {e}")
            return []
    
    def obtener_estadisticas_avanzadas(self):
        """Obtener estadísticas avanzadas para el dashboard"""
        try:
            # Total de predicciones hoy
            fecha_hoy = datetime.utcnow().strftime('%Y-%m-%d')
            inicio_hoy = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            pipeline = [
                {
                    '$match': {
                        'timestamp': {'$gte': inicio_hoy},
                        'action': 'prediction'
                    }
                },
                {
                    '$group': {
                        '_id': '$metadata.sport',
                        'total_predicciones': {'$sum': 1},
                        'usuarios_unicos': {'$addToSet': '$user_id'}
                    }
                }
            ]
            
            resultado = list(self.activity_collection.aggregate(pipeline))
            
            # Procesar resultados
            sports_distribution = {}
            total_predictions = 0
            active_users = set()
            
            for deporte in resultado:
                nombre_deporte = deporte['_id'] or 'desconocido'
                sports_distribution[nombre_deporte] = deporte['total_predicciones']
                total_predictions += deporte['total_predicciones']
                active_users.update(deporte['usuarios_unicos'])
            
            # Calcular porcentajes
            if total_predictions > 0:
                for deporte in sports_distribution:
                    sports_distribution[deporte] = round(
                        (sports_distribution[deporte] / total_predictions) * 100, 
                        1
                    )
            
            metricas = {
                'date': fecha_hoy,
                'total_predictions': total_predictions,
                'active_users': len(active_users),
                'sports_distribution': sports_distribution,
                'timestamp': datetime.utcnow()
            }
            
            return metricas
            
        except Exception as e:
            logger.error(f"Error calculando estadísticas avanzadas: {e}")
            return None
    
    def actualizar_dashboard_automatico(self):
        """Actualizar automáticamente las métricas del dashboard"""
        metricas = self.obtener_estadisticas_avanzadas()
        if metricas:
            return self.guardar_metricas_dashboard(metricas)
        return False