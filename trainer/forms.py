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
            'name', 'team', 'xp', 'pokedex_number',
            'pokemon_caught', 'eggs_hatched', 'kilometers_walked',
            'pokestops_spun', 'research_tasks', 'ace_trainer',
            'battles_won', 'hours_defended', 'berries_fed',
            'great_veteran', 'ultra_veteran', 'master_veteran'
        ]

