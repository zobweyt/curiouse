from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from notifications.signals import notify
import httpagentparser


@receiver(user_logged_in)
def notify_user_of_login(sender, user, request, **kwargs):
    agent = httpagentparser.detect(request.META['HTTP_USER_AGENT'])
    os_name = agent['os']['name']
    browser_name = agent['browser']['name']
    notify.send(recipient=user, sender=user, verb=f'New login in your account from device {os_name} in browser {browser_name} has been detected.')
    