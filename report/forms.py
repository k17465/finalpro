# from urllib.parse import urlparse

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import Widget
from report.models import Users
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text="로그인을 위한 유저 네임", label="username")
    # full_name = forms.CharField(max_length=30, required=True, help_text="회원이름", label="회원 이름")
    email = forms.EmailField(max_length=254, help_text="유효한 메일 주소", label="email주소")
    last_name = forms.CharField(max_length=30, required=True, help_text="성 입력", label="last name")
    first_name = forms.CharField(max_length=30, required=True, help_text="이름 입력", label="first name")

    class Meta:
        model = Users
        fields = (
            "username",
            "email",
            "last_name",
            "first_name",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "유저 네임"})
    )
    password = forms.CharField(
        max_length=100, required=True, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"}),
    )

