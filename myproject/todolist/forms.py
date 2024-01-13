from django import forms
#Greta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group

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