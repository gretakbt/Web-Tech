from django.apps import AppConfig

#https://github.com/divanov11/Django-To-Do-list-with-user-authentication
class BaseConfig(AppConfig):
    name = 'todolist'
#https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
class CalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cal'