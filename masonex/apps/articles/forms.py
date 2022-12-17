from django import forms

from core.utils import DecorateFormFieldsMixin

from articles.models import Article, Category


class ArticleEditorForm(forms.ModelForm):
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
        queryset=Category.objects.only('name'),
        empty_label=None,
        help_text='Choose the most appropriate category for your article.',
        widget=forms.Select(attrs={
            'class': 'selectpicker mb-3',
            'title': 'Select a category',
            'data-live-search': 'true',
            'data-size': 5,
        }),
    )
    thumbnail = forms.ImageField(widget=forms.FileInput(attrs={
        'hidden': True,
        'accept': '.png, .jpg, .jpeg, .webp',
        'data-toggle': 'image',
        'data-target': '#thumbnail',
    }))

    class Meta:
        model = Article
        fields = ('thumbnail', 'title', 'description', 'body', 'category')
        exclude = ('author', 'slug')


class SearchForm(DecorateFormFieldsMixin, forms.Form):
    query = forms.CharField(max_length=64, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    