from typing import Any
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")

        if len(email) >= 350:
            raise forms.ValidationError("Email is too long.")

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ("password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        # Mark email as required

        self.fields["email"].required = True

    # Email validation

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # filtering the email from input in our user model
        # but excluding the user who made the request
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is invalid")

        # len function updated ###

        if len(email) >= 350:
            raise forms.ValidationError("Your email is too long")

        return
