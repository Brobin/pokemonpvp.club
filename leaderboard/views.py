from django.db.models import Avg, Sum, Count
from django.views.generic import TemplateView

from trainer.models import Trainer


class IndexView(TemplateView):
    template_name = 'leaderboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['stats'] = Trainer.objects.aggregate(
            avg_xp=Avg('xp'),
            sum_xp=Sum('xp'),
            avg_pokemon_caught=Avg('pokemon_caught'),
            sum_pokemon_caught=Sum('pokemon_caught'),
            avg_pokestops_spun=Avg('pokestops_spun'),
            sum_pokestops_spun=Sum('pokestops_spun'),
            avg_pokedex_number=Avg('pokedex_number'),
            sum_kilometers_walked=Sum('kilometers_walked'),
            avg_kilometers_walked=Avg('kilometers_walked'),
            sum_battles_won=Sum('battles_won'),
            avg_battles_won=Avg('battles_won'),
            sum_berries_fed=Sum('berries_fed'),
            avg_berries_fed=Avg('berries_fed'),
            sum_hours_defended=Sum('hours_defended'),
            avg_hours_defended=Avg('hours_defended'),
            sum_eggs_hatched=Sum('eggs_hatched'),
            avg_eggs_hatched=Avg('eggs_hatched'),
        )
        context['globes'] = context['stats']['sum_kilometers_walked'] / 40075
        context['xp_leaders'] = Trainer.objects.order_by('-xp')[:5]
        context['pokedex_leaders'] = Trainer.objects.order_by('-pokedex_number', '-xp')[:5]
        context['catch_leaders'] = Trainer.objects.order_by('-pokemon_caught', '-xp')[:5]
        context['spin_leaders'] = Trainer.objects.order_by('-pokestops_spun', '-xp')[:5]
        context['walking_leaders'] = Trainer.objects.order_by('-kilometers_walked', '-xp')[:5]
        context['battle_leaders'] = Trainer.objects.order_by('-battles_won', '-xp')[:5]
        context['egg_leaders'] = Trainer.objects.order_by('-eggs_hatched', '-xp')[:5]
        context['defender_leaders'] = Trainer.objects.order_by('-hours_defended', '-xp')[:5]
        context['berry_leaders'] = Trainer.objects.order_by('-berries_fed', '-xp')[:5]
        context['charts']= self.get_charts()

        return context

    def chart_aggregate(self, team):
        return Trainer.objects.filter(team=team).aggregate(
            players=Count('pk'),
            xp=Sum('xp'),
            pokemon_caught=Sum('pokemon_caught'),
            pokestops_spun=Sum('pokestops_spun'),
            kilometers_walked=Sum('kilometers_walked'),
            battles_won=Sum('battles_won'),
            eggs_hatched=Sum('eggs_hatched'),
            hours_defended=Sum('hours_defended'),
            berries_fed=Sum('berries_fed'),
        )

    def get_charts(self):
        mystic = self.chart_aggregate(Trainer.MYSTIC)
        valor = self.chart_aggregate(Trainer.VALOR)
        instinct = self.chart_aggregate(Trainer.INSTINCT)
        charts = {}
        for datum in ['xp', 'pokemon_caught', 'pokestops_spun',
                      'kilometers_walked', 'battles_won', 'eggs_hatched', 
                      'hours_defended', 'berries_fed']:
            m, v, i = int(mystic[datum] or 0), int(valor[datum] or 0), int(instinct[datum] or 0)
            total = m + v + i
            if total == 0 or m == 0 or v == 0 or i == 0:
                return []
            m = m / mystic['players']
            v = v / valor['players']
            i = i / instinct['players']
            total = m + v + i
            charts[datum] = {
                'mystic': int(m),
                'valor': int(v),
                'instinct': int(i),
                'mystic_pct': m / total * 100,
                'valor_pct': v / total * 100,
                'instinct_pct': i / total * 100,
            }
        total = Trainer.objects.count()
        charts['players'] = {
            'mystic': mystic['players'],
            'valor': valor['players'],
            'instinct': instinct['players'],
            'mystic_pct': mystic['players'] / total * 100,
            'valor_pct': valor['players'] / total * 100,
            'instinct_pct': instinct['players'] / total * 100,
        }
        return charts
