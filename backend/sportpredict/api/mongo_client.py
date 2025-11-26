"""
Cliente MongoDB unificado para la API - Conecta con código de tu amigo en db/
"""
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.db.mongodb import mongo_db, AnalyticsManager, PartidoStatsManager

# ✅ EXPORTAR para uso directo en vistas
mongo_db = mongo_db

# ✅ FUNCIONES DE CONVENIENCIA
def log_user_activity(user_id, action, metadata=None):
    """Registrar actividad usando AnalyticsManager del amigo"""
    try:
        analytics = AnalyticsManager()
        return analytics.registrar_actividad_usuario(user_id, action, metadata)
    except Exception as e:
        print(f"❌ Error con AnalyticsManager: {e}")
        # Fallback
        return mongo_db.user_activity_logs.insert_one({
            'user_id': str(user_id),
            'action': action,
            'timestamp': datetime.utcnow(),
            'metadata': metadata or {}
        })

def get_dashboard_metrics():
    """Obtener métricas del dashboard"""
    try:
        analytics = AnalyticsManager()
        return analytics.obtener_metricas_dashboard()
    except Exception as e:
        print(f"❌ Error obteniendo dashboard: {e}")
        return None

def update_dashboard_auto():
    """Actualizar dashboard automáticamente"""
    try:
        analytics = AnalyticsManager()
        return analytics.actualizar_dashboard_automatico()
    except Exception as e:
        print(f"❌ Error actualizando dashboard: {e}")
        return False

# ✅ ACCESO DIRECTO A LOS MANAGERS
def get_analytics_manager():
    return AnalyticsManager()

def get_stats_manager():
    return PartidoStatsManager()
