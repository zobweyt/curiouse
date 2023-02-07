from django import forms

from core.utils import DecorateFormFieldsMixin
from articles.models import Article, Category


class ArticleEditorForm(DecorateFormFieldsMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.only('name'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select tomselected',
            'data-bs-toggle': 'tom-select',
            'placeholder': 'Select a category'
        }),
    )

    class Meta:
        model = Article
        fields = ('thumbnail', 'title', 'description', 'body', 'category')
        exclude = ('author', 'slug')
        labels = {'thumbnail': ''}
        help_texts = {
            'title': "The title will be shown on the article's page."
        }
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'This article is about...',
                'class': 'fw-medium',
                'data-bs-toggle': 'autosize'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Briefly introduce the contents of the article',
                'data-bs-toggle': 'autosize'
            }),
            'thumbnail': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#thumbnail',
            })
        }
    