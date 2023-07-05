from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Required. Input a valid email address")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email address {email} is already in use.")
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")
    



class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "password")

        
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username'].lower()
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid Login")



class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email', 'bio', 'profile_link1_text', 'profile_link1', 'profile_link2_text', 'profile_link2')

    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email address {email} is already in use.")
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")
    
    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        account.bio = self.cleaned_data['bio']
        account.profile_link1_text = self.cleaned_data['profile_link1_text']
        account.profile_link1 = self.cleaned_data['profile_link1']
        account.profile_link2_text = self.cleaned_data['profile_link2_text']
        account.profile_link2 = self.cleaned_data['profile_link2']
        if commit:
            account.save()
        return account