from django import forms
#Greta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from .models import *

# Reordering Form and View


class PositionForm(forms.Form):
    position = forms.CharField()

#Greta
class ResetPasswordForm(forms.Form): 
    email = forms.EmailField()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_lower = email.lower()
        if User.objects.filter(email__iexact=email_lower).exists():
            self.add_error('username', forms.ValidationError('Diese E-Mail-Adresse ist bereits registriert.'))
        return email


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']



class EventForm(ModelForm):
    

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