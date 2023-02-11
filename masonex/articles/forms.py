from django import forms

from articles.models import Article, Category


class ArticleEditorForm(forms.ModelForm):
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
        fields = ('thumbnail', 'title', 'body', 'category')
        exclude = ('author', 'slug')
        labels = {'thumbnail': ''}
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'This article is about...',
                'class': 'form-control-plaintext h1',
                'data-bs-toggle': 'autosize',
            }),
            'thumbnail': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#thumbnail',
            })
        }
    