from django import forms
#Greta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from .models import *


#https://github.com/divanov11/Django-To-Do-list-with-user-authentication
class PositionForm(forms.Form):
    position = forms.CharField()


class ResetPasswordForm(forms.Form): #eigene Anpassung
    email = forms.EmailField()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):   #eigene Anpassung Emailversand                   
        email = self.cleaned_data.get('email')
        email_lower = email.lower()
        if User.objects.filter(email__iexact=email_lower).exists():
            self.add_error('username', forms.ValidationError('Diese E-Mail-Adresse ist bereits registriert.'))
        return email


class CreateGroupForm(forms.ModelForm): #copy und paste plus Anpassung aus voherig existierenden forms
    class Meta:
        model = Group
        fields = ['name']



class EventForm(ModelForm): # Klasse aus https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html mit Anpassung der User
    

    class Meta:
        model = Event
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),

        }
        fields = '__all__'

    users = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.SelectMultiple(attrs={'autocomplete': 'off'}),
            label="Participants",
            required = False
        )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['bg_color'].widget.attrs['readonly'] = False