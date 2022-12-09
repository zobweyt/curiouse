from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from core.utils import DecorateInputsMixin

from .models import User


class SignUpForm(DecorateInputsMixin, UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class SignInForm(DecorateInputsMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def get_invalid_login_error(self):
        return ValidationError('Incorrect username or password.')


class UserSettingsForm(DecorateInputsMixin, forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'hidden': True, 
            'accept': '.png, .jpg, .jpeg', 
            'data-toggle': 'change-image', 
            'data-target': '#avatar'
        }))
    remove_photo = forms.BooleanField(
        label='Delete photo?', 
        help_text='This action cannot be undone.', 
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'btn-check',
            'onchange': 'this.form.submit();'
        }))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5}))

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        if self.cleaned_data.get('remove_photo'):
            user.avatar.delete()
        return user

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'bio')


class UserPasswordChangeForm(DecorateInputsMixin, PasswordChangeForm):
    pass


class UserEmailChangeForm(DecorateInputsMixin, forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        email = self.cleaned_data['email']
        self.user.email = email
        if commit:
            self.user.save()
        return self.user
