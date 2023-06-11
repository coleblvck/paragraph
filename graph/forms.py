from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from account.models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ["username", "email", "password1", "password2"]

    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        lowercase_username = username.lower()

        return lowercase_username



class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        not_low_username = self.cleaned_data.get('username')
        lowercase_username = not_low_username.lower()
        username = lowercase_username

        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not Account.objects.filter(username=lowercase_username):
            raise forms.ValidationError("Sorry, that username does not exist. Please try again.")
        
        if not Account or not Account.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again, or check your password.")
        return self.cleaned_data

    def login(self, request):
        not_low_username = self.cleaned_data.get('username')
        lowercase_username = not_low_username.lower()
        username = lowercase_username
        
        password = self.cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)
        return user