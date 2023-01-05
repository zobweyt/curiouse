from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


@register.simple_tag(takes_context=True)
def user_avatar(context, user=None, css_class="rounded-circle", width="auto", height="auto"):
    if not user:
        user = context["request"].user

    avatar = user.avatar

    if not avatar:
        url = staticfiles_storage.url("images/user.svg")
    else:
        url = avatar.url

    return mark_safe(f"""
    <img src="{url}" class="{css_class}" style="width: {width}; height: {height};"></img>
    """)


@register.inclusion_tag("widgets/alert.html")
def alert(style, content):
    return {
        "style": style,
        "content": content
    }


@register.inclusion_tag("widgets/delete-confirm-modal.html")
def delete_confirm_modal(object_name, delete_url):    
    return {
        "object_name": object_name,
        "delete_url": delete_url
    }
