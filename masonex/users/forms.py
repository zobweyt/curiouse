from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from core.utils import DecorateFormFieldsMixin
from .models import User


class SignUpForm(DecorateFormFieldsMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        labels = {
            'password1': 'Password',
            'password2': 'Confirm password'
        }


class SignInForm(DecorateFormFieldsMixin, AuthenticationForm):
    error_messages = {
        'invalid_login': 'Incorrect username or password.'
    }


class ProfileUpdateForm(DecorateFormFieldsMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'username', 'bio')
        help_texts = {
            'username': None
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Describe your activities',
                'data-bs-toggle': 'autosize'
            }),
            'avatar': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#avatar'
            })
        }


class UserEmailChangeForm(DecorateFormFieldsMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'autofocus': True
            })
        }


class UserPasswordChangeForm(DecorateFormFieldsMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
