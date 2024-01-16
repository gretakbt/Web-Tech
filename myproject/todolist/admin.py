from django.contrib import admin
from .models import Task, Group, Event

admin.site.register(Event)
admin.site.register(Task)
admin.site.register(Group)