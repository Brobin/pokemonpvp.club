from django import template

from pokemon.models import TypeMatchup


register = template.Library()


@register.filter(name='effectiveness')
def effectiveness(attacking, pokemon):
    effectiveness = TypeMatchup.objects.get(
        attacking_type=attacking,
        defending_type=pokemon.primary_type
    ).multiplier
    if pokemon.secondary_type:
        effectiveness *= TypeMatchup.objects.get(
            attacking_type=attacking,
            defending_type=pokemon.secondary_type
        ).multiplier
    return effectiveness


@register.filter
def percentage(value):
    return str(int(value*100)) + "%"

