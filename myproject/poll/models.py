from django.db import models
from django.contrib.auth.models import User
from todolist.models import Group

class Poll(models.Model):
    question = models.TextField(max_length=105)
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)

    group = models.ForeignKey(Group, related_name='group_polls', null=True, blank=True, on_delete=models.SET_NULL)#angepasst

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count