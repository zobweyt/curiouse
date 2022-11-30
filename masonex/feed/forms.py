from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from feed.models import Post, User, Category
from feed.utils import CharFieldCSSClassMixin


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title based on content',
        'class': 'form-inline-control bg-light fw-medium fs-6',
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Description',
        'class': 'form-inline-control bg-light',
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(attrs={
            'class': 'selectpicker mb-3',
            'title': 'Select a category',
            'data-live-search': 'true',
            'data-size': 5,
        }),
        empty_label=None,
        help_text='Choose the most appropriate category for your post.'
    )
    thumbnail = forms.ImageField(widget=forms.FileInput(attrs={
        'hidden': True,
        'accept': '.png, .jpg, .jpeg, .webp',
        'data-toggle': 'change-image',
        'data-target': '#thumbnail',
    }))

    class Meta:
        model = Post
        fields = ('thumbnail', 'title', 'description', 'body', 'category')
        exclude = ('author', 'slug')


class UserRegistrationForm(CharFieldCSSClassMixin, UserCreationForm):
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class SearchForm(CharFieldCSSClassMixin, forms.Form):
    query = forms.CharField(max_length=64, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))


class UserLoginForm(CharFieldCSSClassMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def get_invalid_login_error(self):
        return ValidationError('Incorrect username or password.')


class ProfileForm(CharFieldCSSClassMixin, forms.ModelForm):
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


class UserPasswordChangeForm(CharFieldCSSClassMixin, PasswordChangeForm):
    pass


class UserEmailChangeForm(CharFieldCSSClassMixin, forms.Form):
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
    