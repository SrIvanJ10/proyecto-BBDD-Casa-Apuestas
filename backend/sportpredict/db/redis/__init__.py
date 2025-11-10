from .sessions import SessionManager

# Crear instancia global
session_manager = SessionManager()

__all__ = ['session_manager']