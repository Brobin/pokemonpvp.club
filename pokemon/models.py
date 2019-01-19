from django.db import models
from django.utils.functional import cached_property

from base.models import BaseModel

from math import floor

from .constants import CPM


class Type(BaseModel):
    name = models.CharField(max_length=12)

    def __str__(self):
        return self.name.title()


class Pokemon(BaseModel):
    number = models.IntegerField()
    name = models.CharField(max_length=32)
    base_attack = models.IntegerField()
    base_defense = models.IntegerField()
    base_stamina = models.IntegerField()
    primary_type = models.ForeignKey(Type,
        on_delete=models.DO_NOTHING,
        related_name='primary_typed')
    secondary_type = models.ForeignKey(Type, blank=True, null=True,
        on_delete=models.DO_NOTHING,
        related_name='secondary_typed')

    @cached_property
    def primary_type_name(self):
        return str(self.primary_type)

    @cached_property
    def secondary_type_name(self):
        if self.secondary_type:
            return str(self.secondary_type)
        return None

    def attack(self, level, att_iv):
        return (self.base_attack + att_iv) * CPM[level]

    def defense(self, level, def_iv):
        return (self.base_defense + def_iv) * CPM[level]

    def stamina(self, level, sta_iv):
        return (self.base_stamina + sta_iv) * CPM[level]

    def cp(self, *args):
        return self.all_stats(*args)[0]

    def stat_sum(self, *args):
        return self.all_stats(*args)[1]

    def stat_product(self, *args):
        return self.all_stats(*args)[2]

    def all_stats(self, level, att_iv, def_iv, sta_iv):
        _att = self.attack(level, att_iv)
        _def = self.defense(level, def_iv)
        _sta = self.stamina(level, sta_iv)
        cp = int(max(floor(_att * _def**0.5 *  _sta**0.5) / 10, 10))
        return cp, floor(sum([_att, _def, _sta])), floor(_att * _def * _sta)

    @cached_property
    def max_cp(self):
        return self.cp(40, 15, 15, 15)

    @cached_property
    def max_stat_sum(self):
        return self.stat_sum(40, 15, 15, 15)

    @cached_property
    def max_stat_product(self):
        return self.stat_product(40, 15, 15, 15)

    def __str__(self):
        return '#{0} {1}'.format(self.number, self.name)

    class Meta:
        verbose_name_plural = 'Pokemon'
