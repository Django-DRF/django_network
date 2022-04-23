from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def check_if_liked(context, post):
    user = context['request'].user

    return post.likes.filter(created_by=user)
