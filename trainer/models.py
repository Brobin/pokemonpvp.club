from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import BaseModel

from .managers import TrainerManager


class Trainer(BaseModel):
    MYSTIC = 1
    VALOR = 2
    INSTINCT = 3
    TEAMS = (
        (MYSTIC, 'Mystic'),
        (VALOR, 'Valor'),
        (INSTINCT, 'Instinct'),
    )
    objects = TrainerManager()

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='trainer',
        on_delete=models.CASCADE)
    name = models.CharField('Trainer Name', max_length=64, unique=True)
    team = models.IntegerField(choices=TEAMS)

    # Experience
    xp = models.BigIntegerField('Total XP')

    # Pokedex Medals
    kanto = models.IntegerField('Kanto', help_text='Kanto Pokedex Entries')
    johto = models.IntegerField('Johto', help_text='Johto Pokedex Entries')
    hoenn = models.IntegerField('Hoenn', help_text='Hoenn Pokedex Entries')
    sinnoh = models.IntegerField('Sinnoh', help_text='Sinnoh Pokedex Entries')

    # PVP League Medals
    great_veteran = models.IntegerField('Great League Veteran')
    ultra_veteran = models.IntegerField('Ultra League Veteran')
    master_veteran = models.IntegerField('Master League Veteran')

    # Required Medals
    jogger = models.IntegerField('Jogger', help_text='Kilometers Walked')
    collector = models.IntegerField('Collector', help_text='Pokemon Caught')
    breeder = models.IntegerField('Breeder', help_text='Eggs Hatched')

    # Optional Medals
    scientist = models.IntegerField('Scientist',help_text='Pokemon Evolved', blank=True, null=True)
    backpacker = models.IntegerField('Backpacker',help_text='Pokestops Spun', blank=True, null=True)
    battle_girl = models.IntegerField('Battle Girl',help_text='Battles Won', blank=True, null=True)
    youngster = models.IntegerField('Youngster',help_text='Tiny Ratatta', blank=True, null=True)
    pikachu_fan = models.IntegerField('Pikachu Fan',help_text='Pikachu Caught', blank=True, null=True)
    berry_master = models.IntegerField('Berry Master',help_text='Berries Fed', blank=True, null=True)
    gym_leader = models.IntegerField('Gym Leader',help_text='Hours Defended', blank=True, null=True)
    pokemon_ranger = models.IntegerField('Pokemon Ranger',help_text='Field Research Tasks', blank=True, null=True)
    idol = models.IntegerField('Idol',help_text='Best Friends', blank=True, null=True)
    gentleman = models.IntegerField('Gentleman',help_text='Pokemon Traded', blank=True, null=True)
    pilot = models.IntegerField('Pilot',help_text='Trade Distance', blank=True, null=True)
    fisherman = models.IntegerField('Fisherman',help_text='Big Magikarp', blank=True, null=True)
    ace_trainer = models.IntegerField('Ace Trainer',help_text='Ace Trainer', blank=True, null=True)
    unown = models.IntegerField('Unown',help_text='Unown', blank=True, null=True)
    champion = models.IntegerField('Champion',help_text='Raids', blank=True, null=True)
    battle_legend = models.IntegerField('Battle Legend',help_text='Legendary Raids', blank=True, null=True)

    # Type Medals
    schoolkid = models.IntegerField('Schoolkid', help_text='Normal Type', blank=True, null=True)
    black_belt = models.IntegerField('Black Belt', help_text='Fighting Type', blank=True, null=True)
    bird_keepr = models.IntegerField('Bird Keepr', help_text='Flying Type', blank=True, null=True)
    punk_girl = models.IntegerField('Punk Girl', help_text='Poison Type', blank=True, null=True)
    ruin_maniac = models.IntegerField('Ruin Maniac', help_text='Ground Type', blank=True, null=True)
    hiker = models.IntegerField('Hiker', help_text='Rock Type', blank=True, null=True)
    bug_catcher = models.IntegerField('Bug Catcher', help_text='Bug Type', blank=True, null=True)
    hex_maniac = models.IntegerField('Hex Maniac', help_text='Ghost Type', blank=True, null=True)
    depot_agent = models.IntegerField('Depot Agent', help_text='Steel Type', blank=True, null=True)
    kindler = models.IntegerField('Kindler', help_text='Fire Type', blank=True, null=True)
    swimmer = models.IntegerField('Swimmer', help_text='Water Type', blank=True, null=True)
    gardener = models.IntegerField('Gardener', help_text='Grass Type', blank=True, null=True)
    rocker = models.IntegerField('Rocker', help_text='Electric Type', blank=True, null=True)
    psychic = models.IntegerField('Psychic', help_text='Psychic Type', blank=True, null=True)
    skier = models.IntegerField('Skier', help_text='Ice Type', blank=True, null=True)
    dragon_tamer = models.IntegerField('Dragon Tamer', help_text='Dragon Type', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('trainer', kwargs={'name': self.name})

    @property
    def discord_username(self):
        return self.user.username[:-4] + '#' + self.user.username[-4:]

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
