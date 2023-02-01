from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    bio = models.TextField(max_length=196, blank=True)
    avatar = models.ImageField(
        verbose_name='Upload photo',
        upload_to=settings.PHOTOS_PATH,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('articles:author_detail', kwargs={'username': self})
    
    def get_avatar_url(self):
        return self.avatar.url if self.avatar else staticfiles_storage.url('images/user.svg')        

    class Meta:
        ordering = ['username']
