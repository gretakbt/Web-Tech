from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'todolist'
    
class CalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cal'