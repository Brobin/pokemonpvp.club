from rest_framework import serializers

from trainer.models import Trainer
from pokemon.models import Type, Pokemon


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['name']


class PokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pokemon
        fields = [
            'number', 'name', 'base_attack', 'base_defense',
            'base_stamina', 'primary_type_name',  'secondary_type_name',
            'max_cp'
        ]


class TrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = [
            'name', 'discord_username', 'team_name', 'xp', 'level',
            'kanto', 'johto', 'hoenn', 'sinnoh',
            'great_veteran', 'ultra_veteran', 'master_veteran',
            'jogger', 'collector', 'breeder',
            'scientist', 'backpacker', 'battle_girl', 'youngster',
            'pikachu_fan','berry_master', 'gym_leader', 'pokemon_ranger',
            'idol', 'gentleman', 'pilot', 'fisherman', 'ace_trainer',
            'unown', 'champion', 'battle_legend', 'schoolkid',
            'black_belt', 'bird_keepr', 'punk_girl', 'ruin_maniac',
            'hiker', 'bug_catcher', 'hex_maniac', 'depot_agent',
            'kindler', 'swimmer', 'gardener', 'rocker', 'psychic',
            'skier', 'dragon_tamer', 'delinquent', 'fairy_tale_girl'
        ]