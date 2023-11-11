from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    username = forms.CharField(
            label = "Username*",
            help_text = "",
            required = True,
            widget = forms.TextInput(attrs={
                "name":"username",
                "placeholder":"Username",
                })
            )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.TextInput(attrs={
            "name": "email",
            "type": "email",
            "placeholder": "Email"
        })
    )

    password1 = forms.CharField(
        label="Password*",
        required=True,
        help_text = "",
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "name": "password1",
            "id": "password",
            "placeholder": "Password"
        })
    )

    password2 = forms.CharField(
        label="Password Confirmation*",
        required=True,
        help_text = "",
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "name": "password2",
            "id": "password",
            "placeholder": "Password Confirmation"
        })
    )

    class Meta:
        model = User
        fields = ("username","email","password1","password2",)

