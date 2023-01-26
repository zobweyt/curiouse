from django import forms

from core.utils import DecorateFormFieldsMixin
from articles.models import Article, Category


class ArticleEditorForm(DecorateFormFieldsMixin, forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'This article is about...',
        'class': 'fw-medium mt-1'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder': 'Briefly introduce the contents of the article',
        'class': 'resize-none'
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.only('name'),
        empty_label=None,
        widget=forms.Select(attrs={
            'required': 'true',
            'title': 'Choose category',
            'data-size': 5,
            'data-live-search': 'true',
            'data-style': 'btn-sm btn-muted w-auto',
            'class': 'selectpicker',
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
    query = forms.CharField(max_length=64, required=True)
    