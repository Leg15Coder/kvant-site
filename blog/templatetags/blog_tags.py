from django import template
from ..models import *

register = template.Library()

@register.simple_tag()
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None

@register.inclusion_tag('navnar.html')
def my_avatar(user=None, user2=None):
  return {'avatar': Profile.objects.get(owner = user).icon.url}

my_avatar = register.tag(my_avatar)