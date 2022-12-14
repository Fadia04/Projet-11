from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class allowed to the registration of the users"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
