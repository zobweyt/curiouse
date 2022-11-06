from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from masonex.settings import PHOTOS_PATH, AUTH_USER_MODEL


class User(AbstractUser):
    bio = models.TextField(max_length=256, blank=True)
    photo = models.ImageField(upload_to=PHOTOS_PATH, null=True, blank=True) 

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    slug = models.SlugField(max_length=64, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name', 'pk']


class Post(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=128, db_index=True)
    slug = AutoSlugField(populate_from='title', db_index=True)
    description = models.CharField(max_length=512, db_index=True)
    photo = models.ImageField(upload_to=PHOTOS_PATH) # cover_photo or cover
    body = RichTextField()
    likes = models.ManyToManyField(AUTH_USER_MODEL, related_name='likes', related_query_name='like')
    create_date = models.DateTimeField(auto_now_add=True) # time_create
    update_date = models.DateTimeField(auto_now=True) # time_update

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk, 'post_slug': self.slug})

    class Meta:
        ordering = ['-create_date', 'title']
