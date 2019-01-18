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
            avg_collector=Avg('collector'),
            sum_collector=Sum('collector'),
            avg_breeder=Avg('breeder'),
            sum_breeder=Sum('breeder'),
        )
        context['xp_leaders'] = Trainer.objects.order_by('-xp')[:5]
        context['collector_leaders'] = Trainer.objects.order_by('-collector', '-xp')[:5]
        context['breeder_leaders'] = Trainer.objects.order_by('-breeder', '-xp')[:5]
        context['charts']= self.get_charts()

        return context

    def chart_aggregate(self, team):
        return Trainer.objects.filter(team=team).aggregate(
            players=Count('pk'),
            xp=Sum('xp'),
            collector=Sum('collector'),
            breeder=Sum('breeder')
        )

    def get_charts(self):
        mystic = self.chart_aggregate(Trainer.MYSTIC)
        valor = self.chart_aggregate(Trainer.VALOR)
        instinct = self.chart_aggregate(Trainer.INSTINCT)
        charts = {}
        for datum in ['xp', 'collector', 'breeder']:
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
