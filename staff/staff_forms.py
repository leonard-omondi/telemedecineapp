from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:  # Specifies which model it will interact with
        model = User
        fields = ['username', 'email', 'password1', 'password2']
