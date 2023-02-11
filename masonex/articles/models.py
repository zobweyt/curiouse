from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

from django_editorjs_fields import EditorJsJSONField


class Category(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    slug = models.SlugField(max_length=64, null=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name', 'pk']


class Article(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, null=True, db_index=True)
    thumbnail = models.ImageField(upload_to=settings.PHOTOS_PATH)
    body = EditorJsJSONField(**settings.EDITORJS_CONFIG_OVERRIDE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['-created_at', 'title', 'slug', 'pk']
