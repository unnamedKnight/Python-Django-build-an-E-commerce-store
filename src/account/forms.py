from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CreateUserForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists')

        if len(email >= 350):
            raise forms.ValidationError('Email is too long.')