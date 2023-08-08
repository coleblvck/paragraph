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
        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")
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
                raise forms.ValidationError("Sorry, that login was invalid. Please try again, or check your details.")



class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'hide_email', 'tagline', 'bio', 'profile_link1_text', 'profile_link1', 'profile_link2_text', 'profile_link2')

    
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")
    
    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.hide_email = self.cleaned_data['hide_email']
        account.tagline = self.cleaned_data['tagline']
        account.bio = self.cleaned_data['bio']
        account.profile_link1_text = self.cleaned_data['profile_link1_text']
        account.profile_link1 = self.cleaned_data['profile_link1']
        account.profile_link2_text = self.cleaned_data['profile_link2_text']
        account.profile_link2 = self.cleaned_data['profile_link2']
        if commit:
            account.save(update_fields=['username', 'hide_email', 'tagline', 'bio', 'profile_link1_text', 'profile_link1', 'profile_link2_text', 'profile_link2'])
        return account
    


class ImageUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('profile_image', 'username', 'hide_email', 'tagline', 'bio', 'profile_link1_text', 'profile_link1', 'profile_link2_text', 'profile_link2')    
    
    def save(self, commit=True):
        account = super(ImageUpdateForm, self).save(commit=False)
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save(update_fields=['profile_image'])
        return account