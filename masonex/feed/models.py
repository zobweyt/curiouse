from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
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


class Post(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=128, db_index=True)
    slug = AutoSlugField(populate_from='title', db_index=True)
    description = models.CharField(max_length=256, db_index=True)
    thumbnail = models.ImageField(upload_to=PHOTOS_PATH)
    body = EditorJsJSONField(**EDITORJS_CONFIG)
    likes = models.ManyToManyField(AUTH_USER_MODEL, related_name='likes', related_query_name='like')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.pk, 'post_slug': self.slug})

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-created_at', 'title', 'description', 'slug', 'pk']


class User(AbstractUser):
    bio = models.TextField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to=PHOTOS_PATH, null=True, blank=True)
    bookmarks = models.ManyToManyField(Post, related_name='bookmarks', related_query_name='bookmark', blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.username})

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['username']
