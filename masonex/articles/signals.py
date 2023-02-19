from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Author


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
