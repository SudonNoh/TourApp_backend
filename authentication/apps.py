from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    label = 'authentication'
    verbose_name: str = 'Authentication'
        
    def ready(self):
        import authentication.signals
        
default_app_config = 'authentication.AuthenticationConfig'