from core.sessions import AuthenticationSession
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def authenticationTag(context):
    tokens = AuthenticationSession(context['request'])
    response = tokens.verifyAccessToken('pen3')
    return True if response else False
