from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    """
    Action model describing the actor acting out a verb on
    an optional action object referenced to a target.
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/
    
    Generalized Format::
    
        <actor> <verb> <target> <created_at>
        <actor> <verb> <action_object> <target> <created_at>
        
    Examples::
    
        <Elizabeth Spark> <started following you!> <27 minutes ago>
        <Kirsten Nunez> <has just published a new article:> <Cooking delicious soup> <1 day ago>
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipient',
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='actor',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=128)
    action_object_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='action_object_content_type',
        blank=True,
        null=True
    )
    action_object_object_id = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    action_object = GenericForeignKey(
        'action_object_content_type',
        'action_object_object_id'
    )
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='target_content_type'
    )
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey(
        'target_content_type',
        'target_object_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        actor_name = self.actor.get_full_name()
        action_object = self.action_object or ''
        return f'{actor_name} {self.verb} {action_object}'
