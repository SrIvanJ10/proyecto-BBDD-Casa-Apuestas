from django.apps import AppConfig

class SportpredictConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sportpredict'

    def ready(self):
        import sportpredict.signals
