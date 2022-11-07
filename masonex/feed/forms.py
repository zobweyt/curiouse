from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from feed.models import Post, User, Category
from feed.utils import FormControlMixin


class PostForm(FormControlMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Not selected'

    class Meta:
        model = Post
        fields = ('thumbnail', 'title', 'description', 'body', 'category')
        exclude = ('author', 'slug')


class UserRegistrationForm(FormControlMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


POST_ORDER_CHOICES = [
    ('category', 'Category'),
    ('-created_at', 'Create date'),
    ('-modified_at', 'Update date'),
]


class SearchForm(forms.Form):
    query = forms.CharField(max_length=128)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    published = forms.ChoiceField(choices=[
        ('today', 'Today'),
        ('week', 'This week'),
        ('month', 'This month'),
        ('year', 'This year')
    ])
    order_by = forms.ChoiceField(choices=POST_ORDER_CHOICES)


class UserLoginForm(FormControlMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def get_invalid_login_error(self):
        return ValidationError('Incorrect username or password.')


class ProfileForm(FormControlMixin, forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'hidden': True, 'accept': '.png, .jpg, .jpeg', 'data-toggle': 'change-avatar', 'data-target': '#avatar'}), required=False)
    remove_photo= forms.BooleanField(required=False)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)

    def save(self, *args, **kwargs):
        user = super(self.__class__, self).save(*args, **kwargs)
        if self.cleaned_data.get('remove_photo'):
            user.avatar.delete()
        return user

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'bio')
