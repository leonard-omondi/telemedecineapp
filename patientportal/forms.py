from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PatientRegisterForm(UserCreationForm):  # Additional fields can be added to the form here
    email = forms.EmailField()

    class Meta:  # Specifies the model we want our form to interact with
        model = User  # When the form validates, a new user is created.
        fields = ['username', 'email', 'password1', 'password2']  # Fields that will be on our form
