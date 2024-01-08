from django.db import models
from django.urls import reverse
# Create your models here.


COLOR_CHOICES = (
    ('#5549A3', 'Purple'),
    ('#6d6c6c', 'Grey'),
    ('#2323a0', 'Blue'),
    ('#940D23', 'Red'),
    ('#179213', 'Green'),
)

class Event(models.Model):

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
        path = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{path}"> {start_time}-{end_time} {self.title} </a>'
