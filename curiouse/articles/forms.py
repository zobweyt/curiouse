from django import forms

from articles.models import Article


class ArticleEditorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ''

    class Meta:
        model = Article
        fields = ('thumbnail', 'title', 'body', 'categories')
        exclude = ('author', 'slug')
        labels = {
            'title': '',
        }
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'This article is about...',
                'class': 'form-control-plaintext h1',
                'data-bs-toggle': 'autosize',
            }),
            'categories': forms.SelectMultiple(attrs={
                'placeholder': 'Type to search...',
                'data-bs-toggle': 'tom-select',
            }),
            'thumbnail': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#thumbnail',
                'data-style': 'flex-fill rounded-4',
            })
        }
    