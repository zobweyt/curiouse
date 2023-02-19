from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings


class User(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(help_text='The account recovery email.')
    bio = models.TextField(max_length=196, blank=True)
    avatar = models.ImageField(
        verbose_name='Upload photo',
        upload_to=settings.PHOTOS_PATH,
        blank=True,
        null=True
    )
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    
    def get_avatar_url(self):
        return self.avatar.url if self.avatar else staticfiles_storage.url('images/user.svg')

    class Meta:
        ordering = ['username', 'is_active']
