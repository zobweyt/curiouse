from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from feed.models import Post, User, Category
from feed.utils import CharFieldCSSClassMixin


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title based on content',
        'class': 'border-0 d-block bg-light mt-2 form-control form-control-sm',
        }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Description',
        'class': 'border-0 d-block bg-light mt-2 form-control form-control-sm',
        }))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Not selected'

    class Meta:
        model = Post
        fields = ('thumbnail', 'title', 'description', 'body', 'category')
        exclude = ('author', 'slug')


class UserRegistrationForm(CharFieldCSSClassMixin, UserCreationForm):
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
        'data-toggle': 'change-avatar', 
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
    bio = forms.CharField(
        help_text='Adding a profile bio can help us promote you!', 
        required=False,
        widget=forms.Textarea(attrs={'rows': 5}))

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
    