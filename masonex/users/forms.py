from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from core.utils import DecorateFormFieldsMixin
from .models import User


class SignUpForm(DecorateFormFieldsMixin, UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'autofocus': True}))
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class SignInForm(DecorateFormFieldsMixin, AuthenticationForm):
    error_messages = {'invalid_login': 'Incorrect username or password.'}


class ProfileUpdateForm(DecorateFormFieldsMixin, forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describe your activities'
            }),
            'avatar': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#avatar'
            })
        }


class UserEmailChangeForm(DecorateFormFieldsMixin, forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

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
    
    class Meta:
        help_texts = {
            'new_password1': None
        }


__all__ = [
    'SignUpForm',
    'SignInForm',
    'ProfileUpdateForm',
    'UserEmailChangeForm',
    'UserPasswordChangeForm',
]
