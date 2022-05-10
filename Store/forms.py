import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=200)
    first_name = forms.CharField(max_length=30)
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    phone_number = forms.CharField(required=False)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),
        label=("Date of birth"), initial=datetime.date.today, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'birth_date', 'phone_number')


