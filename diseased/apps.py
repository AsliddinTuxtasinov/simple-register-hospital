from django.apps import AppConfig


class DiseasedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diseased'

    def ready(self):
        import diseased.signals
