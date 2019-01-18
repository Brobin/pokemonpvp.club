from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import BaseModel


class Trainer(BaseModel):
    MYSTIC = 1
    VALOR = 2
    INSTINCT = 3
    TEAMS = (
        (MYSTIC, 'Mystic'),
        (VALOR, 'Valor'),
        (INSTINCT, 'Instinct'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='trainer',
        on_delete=models.CASCADE)
    name = models.CharField('Trainer Name', max_length=64, unique=True)
    team = models.IntegerField(choices=TEAMS)

    xp = models.BigIntegerField('Total XP')
    pokedex_number = models.IntegerField('Pokedex Entries')

    pokemon_caught = models.IntegerField('Pokemon Caught')
    eggs_hatched = models.IntegerField('Eggs Hatched')
    kilometers_walked = models.FloatField('Kilometers Walked')

    pokestops_spun = models.IntegerField('Pokestops Spun')
    research_tasks = models.IntegerField('Research Tasks')
    ace_trainer = models.IntegerField('Ace Trainer')

    battles_won = models.IntegerField('Battles Won')
    hours_defended = models.IntegerField('Hours Defended')
    berries_fed = models.IntegerField('Berries Fed')

    great_veteran = models.IntegerField('Great League Veteran')
    ultra_veteran = models.IntegerField('Ultra League Veteran')
    master_veteran = models.IntegerField('Master League Veteran')

    def get_absolute_url(self):
        return reverse('trainer', kwargs={'name': self.name})

    @property
    def discord_username(self):
        discord = self.user.socialaccount_set.first()
        try:
            return '{username}#{discriminator}'.format(**discord.extra_data)
        except:
            return ''

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def team_name(self):
        return self.TEAMS[self.team - 1][1]

    @property
    def team_image(self):
        return 'img/{0}.png'.format(self.team_name.lower())

    @property
    def level(self):
        if self.xp >= 20000000:
            return 40
        elif self.xp >= 15000000:
            return 39
        elif self.xp >= 12000000:
            return 38
        elif self.xp >= 9500000:
            return 37
        elif self.xp >= 7500000:
            return 36
        elif self.xp >= 6000000:
            return 35
        elif self.xp >= 4750000:
            return 34
        elif self.xp >= 3750000:
            return 33
        elif self.xp >= 3000000:
            return 32
        elif self.xp >= 2500000:
            return 31
        elif self.xp >= 2000000:
            return 30
        elif self.xp >= 1650000:
            return 29
        elif self.xp >= 1350000:
            return 28
        elif self.xp >= 1100000:
            return 27
        elif self.xp >= 900000:
            return 26
        elif self.xp >= 710000:
            return 25
        elif self.xp >= 560000:
            return 24
        elif self.xp >= 435000:
            return 23
        elif self.xp >= 335000:
            return 22
        elif self.xp >= 260000:
            return 21
        elif self.xp >= 210000:
            return 20
        return "<20"
