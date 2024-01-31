from django.forms import ModelForm
from .models import Poll, Group
from django import forms

#https://prettyprinted.com/tutorials/creating-a-poll-app-in-django

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three', 'group']
        

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id', None)
        super(CreatePollForm, self).__init__(*args, **kwargs)
        # Begrenze die Auswahl auf die angegebene Gruppe
        if group_id:
            self.fields['group'].queryset = Group.objects.filter(id=group_id)
#https://prettyprinted.com/tutorials/creating-a-poll-app-in-django
