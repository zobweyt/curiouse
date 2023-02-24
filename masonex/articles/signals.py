from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from notifications.signals import notify

from .models import Author, Article


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
        

@receiver(m2m_changed, sender=Author.followers.through)
def notify_author_of_follow(sender, instance, action, pk_set, **kwargs):
    if action == 'pre_add':
        followers = Author.objects.filter(pk__in=pk_set)
        for follower in followers:
            notify.send(
                recipient=instance.user,
                sender=follower,
                verb='started following you!',
            )
        

@receiver(post_save, sender=Article)
def notify_followers_of_new_article(sender, instance, created, **kwargs):
    if created:
        for follower in instance.author.followers.all():
            notify.send(
                recipient=follower,
                sender=instance.author,
                verb='has just published new article:',
                action_object=instance,
                description='We advise you to read it!',
            )
