from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings


class User(AbstractUser):
    bio = models.TextField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to=settings.PHOTOS_PATH, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('articles:user', kwargs={'username': self.username})

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['username']
