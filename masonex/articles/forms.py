from django import forms

from articles.models import Article, Category


class ArticleEditorForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('thumbnail', 'title', 'body', 'categories')
        exclude = ('author', 'slug')
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'This article is about...',
                'class': 'form-control-plaintext h1',
                'data-bs-toggle': 'autosize',
                'minlength': 3,
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-select tomselected',
                'data-bs-toggle': 'tom-select',
                'placeholder': 'Type to search...'
            }),
            'thumbnail': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#thumbnail',
            })
        }
    