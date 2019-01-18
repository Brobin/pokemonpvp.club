from rest_framework import serializers

from trainer.models import Trainer


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