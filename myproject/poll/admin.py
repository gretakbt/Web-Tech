from django.contrib import admin

#https://prettyprinted.com/tutorials/creating-a-poll-app-in-django
from .models import Poll
admin.site.register(Poll)