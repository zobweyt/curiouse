from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from notifications.models import Notification

from .models import Author, Article


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
        

@receiver(m2m_changed, sender=Author.followers.through)
def notify_author_of_follow(sender, instance, action, pk_set, **kwargs):
    if instance.user.new_follow_notifications and action == 'pre_add':
        followers = get_user_model().objects.filter(pk__in=pk_set)
        for follower in followers:
            Notification.objects.create(
                recipient=instance.user,
                sender=follower,
                target=follower,
                content=f'started following you!',
            )
        

@receiver(post_save, sender=Article)
def notify_followers_of_new_article(sender, instance, created, **kwargs):
    if created:
        for follower in instance.author.followers.filter(new_article_notifications=True):
            Notification.objects.create(
                recipient=follower,
                sender=instance.author.user,
                target=instance,
                content=f'{instance.author} has just published new article: "{instance}". We advise you to read it.',
            )
