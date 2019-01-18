from django import forms

from .models import Trainer


class TrainerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Trainer
        fields = [
            'name', 'team', 'xp',
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
            'skier', 'dragon_tamer'
        ]
