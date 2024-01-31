from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


#https://github.com/divanov11/Django-To-Do-list-with-user-authentication
class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'

# ab hier erstellen von Group Model unter zuhilfenahme von der Django Dokumentation https://docs.djangoproject.com/en/5.0/topics/db/models/
class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='group_memberships')
    polls = models.ManyToManyField('poll.Poll', related_name='groups_polls', blank=True)

    def __str__(self):
        return self.name
# bis hier erstellen von Group Model unter zuhilfenahme von der Django Dokumentation https://docs.djangoproject.com/en/5.0/topics/db/models/


# Aus https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
COLOR_CHOICES = (
    ('#5549A3', 'Purple'),
    ('#6d6c6c', 'Grey'),
    ('#2323a0', 'Blue'),
    ('#940D23', 'Red'),
    ('#179213', 'Green'),
)

class Event(models.Model): # Klasse aus https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html mit Anpassung der User
    id = models.BigAutoField(primary_key=True)
    users = models.ManyToManyField(User, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    bg_color = models.CharField(max_length=20, choices = COLOR_CHOICES, default = '#5549A3')
    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        start_time = self.start_time.strftime("%I:%M %p")
        end_time = self.end_time.strftime("%I:%M %p")
        path = reverse('event_edit', args=(self.id,))
        return f'<a href="{path}" style="color: white;"> {start_time}-{end_time} {self.title} </a>'
