from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from core.utils import DecorateFormFieldsMixin

from .models import User


# define in models.py?
PASSWORD_HELP_TEXT = 'Come up with a strong password of at least 8 characters.'


class SignUpForm(DecorateFormFieldsMixin, UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'autofocus': True}))
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True, help_text='Short name for Masonex.')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password', 
        required=True, widget=forms.PasswordInput, 
        help_text=PASSWORD_HELP_TEXT)
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class SignInForm(DecorateFormFieldsMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def get_invalid_login_error(self):
        return ValidationError('Incorrect username or password.')


class ProfileUpdateForm(DecorateFormFieldsMixin, forms.ModelForm):
    avatar = forms.ImageField(
        label='Upload photo',
        required=False,
        widget=forms.FileInput(attrs={
            'hidden': True,
            'accept': '.png, .jpg, .jpeg',
            'data-toggle': 'image',
            'data-target': '#avatar'
        }))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Describe your activities'
        }))

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'bio')


class UserEmailChangeForm(DecorateFormFieldsMixin, forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}), 
        help_text='Notifications will be sent to this email.')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        email = self.cleaned_data['email']
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class UserPasswordChangeForm(DecorateFormFieldsMixin, PasswordChangeForm):
    new_password1 = forms.CharField(
        label='New password', 
        widget=forms.PasswordInput(), 
        help_text=PASSWORD_HELP_TEXT)


__all__ = [
    'SignUpForm',
    'SignInForm',
    'ProfileUpdateForm',
    'UserEmailChangeForm',
    'UserPasswordChangeForm',
]
