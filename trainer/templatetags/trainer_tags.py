from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='add_class')
def add_class(field, cls):
    return field.as_widget(attrs={"class": cls})


@register.simple_tag(name='url_replace')
def url_replace(request, field, value):
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()


@register.filter(name='trainer_rank')
def trainer_rank(request, counter):
    base = (int(request.GET.get('page', '1')) - 1) * settings.PAGINATE_BY
    return base + counter
