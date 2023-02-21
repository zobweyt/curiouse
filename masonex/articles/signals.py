from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from notifications.signals import notify

from .models import Author, Follow, Article


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
        
        
@receiver(post_save, sender=Follow)
def notify_author_of_follow(sender, instance, created, **kwargs):
    if created:
        notify.send(
            sender=instance.follower,
            recipient=instance.author.user,
            verb='started following you!',
        )
        

@receiver(post_save, sender=Article)
def notify_followers_of_new_article(sender, instance, created, **kwargs):
    if created:
        for follower in instance.author.followers.all():
            notify.send(
                sender=instance.author,
                recipient=follower.user,
                verb='has just published new article:',
                action_object=instance,
                description='We advise you to read it!',
            )
