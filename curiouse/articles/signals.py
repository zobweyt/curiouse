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
            follower_author = Author.objects.get(user=follower)
            Notification.objects.create(
                recipient=instance.user,
                actor=follower,
                verb=f'started following you!',
                target=follower_author,
            )
        

@receiver(post_save, sender=Article)
def notify_followers_of_new_article(sender, instance, created, **kwargs):
    if created:
        for follower in instance.author.followers.filter(new_article_notifications=True):
            Notification.objects.create(
                recipient=follower,
                actor=instance.author.user,
                verb=f'has just published new article:',
                action_object=instance,
                target=instance,
            )
