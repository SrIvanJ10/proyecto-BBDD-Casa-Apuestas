"""
Cliente Redis unificado para la API
"""
import redis
from django.conf import settings


# Cliente Redis global
redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)


def get_redis_client():
    """Obtener instancia del cliente Redis"""
    return redis_client


def cache_set(key, value, ttl=3600):
    """Guardar valor en caché con TTL"""
    return redis_client.setex(key, ttl, value)


def cache_get(key):
    """Obtener valor del caché"""
    return redis_client.get(key)


def cache_delete(key):
    """Eliminar valor del caché"""
    return redis_client.delete(key)


def cache_exists(key):
    """Verificar si existe una clave en caché"""
    return redis_client.exists(key) == 1
