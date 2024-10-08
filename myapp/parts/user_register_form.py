from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp.models import User

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')
