from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    label = 'users'
    verbose_name: str = 'Users'

    def ready(self):
        import users.API.signals
        
default_app_config = 'users.UserConfig'