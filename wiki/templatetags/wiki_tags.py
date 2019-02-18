from django import template
from django.db.models import Count

from taggit.models import Tag


register = template.Library()


@register.simple_tag(name='url_replace')
def url_replace(request, field, value):  # coverage: omit
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()


@register.inclusion_tag('wiki/tags/_sidebar.html')
def wiki_sidebar():
    return {
        'tags': Tag.objects.annotate(
            articles=Count('taggit_taggeditem_items')
        ).filter(articles__gt=0).order_by( 'name')
    }
