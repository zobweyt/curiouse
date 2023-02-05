from django import forms

from core.utils import DecorateFormFieldsMixin
from articles.models import Article, Category


class ArticleEditorForm(DecorateFormFieldsMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.only('name'),
        empty_label=None,
        widget=forms.Select(attrs={
            'required': 'true',
            'title': 'Choose category',
            'data-size': 4,
            'data-live-search': 'true',
            'data-style': 'btn-sm btn-muted w-auto',
        }),
    )

    class Meta:
        model = Article
        fields = ('thumbnail', 'title', 'description', 'body', 'category')
        exclude = ('author', 'slug')
        labels = {'thumbnail': ''}
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'This article is about...',
                'class': 'fw-medium mt-1'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Briefly introduce the contents of the article',
                'class': 'resize-none'
            }),
            'thumbnail': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#thumbnail',
            })
        }
    