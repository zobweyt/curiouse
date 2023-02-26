from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recipient', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    content = models.TextField(max_length=196)
    created_at = models.DateTimeField(auto_now_add=True)
    # мб target назвать action_object?

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Notification from {self.sender} to {self.recipient}.'
