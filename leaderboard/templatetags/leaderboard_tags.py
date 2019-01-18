import re
from datetime import date, datetime
from decimal import Decimal

from django import template
from django.conf import settings
from django.template import defaultfilters
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.utils.timezone import is_aware, utc
from django.utils.translation import gettext as _, ngettext, pgettext


register = template.Library()


# A tuple of standard large number to their converters
intword_converters = (
    (6, lambda number: (
        ngettext('%(value).2f million', '%(value).2f million', number),
        ngettext('%(value)s million', '%(value)s million', number),
    )),
    (9, lambda number: (
        ngettext('%(value).2f billion', '%(value).2f billion', number),
        ngettext('%(value)s billion', '%(value)s billion', number),
    )),
    (12, lambda number: (
        ngettext('%(value).2f trillion', '%(value).2f trillion', number),
        ngettext('%(value)s trillion', '%(value)s trillion', number),
    )),
    (15, lambda number: (
        ngettext('%(value).2f quadrillion', '%(value).2f quadrillion', number),
        ngettext('%(value)s quadrillion', '%(value)s quadrillion', number),
    )),
    (18, lambda number: (
        ngettext('%(value).2f quintillion', '%(value).2f quintillion', number),
        ngettext('%(value)s quintillion', '%(value)s quintillion', number),
    )),
    (21, lambda number: (
        ngettext('%(value).2f sextillion', '%(value).2f sextillion', number),
        ngettext('%(value)s sextillion', '%(value)s sextillion', number),
    )),
    (24, lambda number: (
        ngettext('%(value).2f septillion', '%(value).2f septillion', number),
        ngettext('%(value)s septillion', '%(value)s septillion', number),
    )),
    (27, lambda number: (
        ngettext('%(value).2f octillion', '%(value).2f octillion', number),
        ngettext('%(value)s octillion', '%(value)s octillion', number),
    )),
    (30, lambda number: (
        ngettext('%(value).2f nonillion', '%(value).2f nonillion', number),
        ngettext('%(value)s nonillion', '%(value)s nonillion', number),
    )),
    (33, lambda number: (
        ngettext('%(value).2f decillion', '%(value).2f decillion', number),
        ngettext('%(value)s decillion', '%(value)s decillion', number),
    )),
    (100, lambda number: (
        ngettext('%(value).2f googol', '%(value).2f googol', number),
        ngettext('%(value)s googol', '%(value)s googol', number),
    )),
)


@register.filter(is_safe=False)
def intword2(value):
    """
    Convert a large integer to a friendly text representation. Works best
    for numbers over 1 million. For example, 1000000 becomes '1.0 million',
    1200000 becomes '1.2 million' and '1200000000' becomes '1.2 billion'.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000000:
        return value

    def _check_for_i18n(value, float_formatted, string_formatted):
        """
        Use the i18n enabled defaultfilters.floatformat if possible
        """
        if settings.USE_L10N:
            value = defaultfilters.floatformat(value, 2)
            template = string_formatted
        else:
            template = float_formatted
        return template % {'value': value}

    for exponent, converters in intword_converters:
        large_number = 10 ** exponent
        if value < large_number * 1000:
            new_value = value / large_number
            return _check_for_i18n(new_value, *converters(new_value))
    return value
