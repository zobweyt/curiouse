from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField

from masonex.settings import PHOTOS_PATH, AUTH_USER_MODEL, EDITORJS_CONFIG


class Category(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    slug = models.SlugField(max_length=64, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name', 'slug', 'pk']


class Article(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=128, db_index=True)
    slug = AutoSlugField(populate_from='title', db_index=True)
    description = models.CharField(max_length=256, db_index=True)
    thumbnail = models.ImageField(upload_to=PHOTOS_PATH)
    body = EditorJsJSONField(**EDITORJS_CONFIG)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_pk': self.pk, 'article_slug': self.slug})

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['-created_at', 'title', 'description', 'slug', 'pk']
