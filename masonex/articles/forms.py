from django import forms

from articles.models import Article, Category


class ArticleEditorForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.only('name'),
        required=True,
        help_text='Categories help Masonex readers explore articles that interest them. Select at least 1 to 3.',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select tomselected',
            'data-bs-toggle': 'tom-select',
            'placeholder': 'Type to search...'
        }),
    )

    class Meta:
        model = Article
        fields = ('thumbnail', 'title', 'body', 'categories')
        exclude = ('author', 'slug')
        labels = {'thumbnail': 'Article listing cover image'}
        help_texts = {
            'thumbnail': 'This image will be displayed on article listing. The recommended size 1920x1440 and recommended ratio is 4:3.'
        }
        widgets = {
            'title': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'This article is about...',
                'class': 'form-control-plaintext h1',
                'data-bs-toggle': 'autosize',
                'minlength': 3,
            }),
            'thumbnail': forms.FileInput(attrs={
                'hidden': True,
                'data-toggle': 'image',
                'data-target': '#thumbnail',
            })
        }
    