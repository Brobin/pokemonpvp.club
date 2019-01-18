from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from math import floor

from .models import Pokemon


class PokemonView(ListView):
    queryset = Pokemon.objects.order_by('number')


class PvpIVSpread(TemplateView):
    template_name = 'pokemon/iv_spread.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['choices'] = Pokemon.objects.order_by('name')
        
        pokemon = self.request.GET.get('pokemon', 'Skarmory')
        max_cp = int(self.request.GET.get('max_cp', 1500))

        try:
            pokemon = Pokemon.objects.get(name=pokemon)
        except Pokemon.DoesNotExist:
            messages.error(self.request, 'Please Choose a valid pokemon')
            pokemon = Pokemon.objects.get(name='Skarmory')

        context['att_iv'] = int(self.request.GET.get('att_iv', 0))
        context['def_iv'] = int(self.request.GET.get('def_iv', 15))
        context['sta_iv'] = int(self.request.GET.get('sta_iv', 14))
        context['ivs'] = range(0, 16)
        context['pokemon'] = pokemon
        context['max_cp'] = max_cp

        key = pokemon.name + str(context['max_cp'])
        combos = cache.get(key)
        if not combos:
            combos = list(self.get_combos(pokemon, max_cp))
            cache.set(key, combos, 60*60*24*7)
        context['combos'] = combos
        max_product = combos[-1][-2]
        context['my_combo'] = self.get_my_combo(
            pokemon, context['att_iv'], context['def_iv'],
            context['sta_iv'], max_cp, max_product)
        return context

    def get_my_combo(self, pokemon, att_iv, def_iv, sta_iv, max_cp, max_product):
        for level in reversed(range(20, 81)):
            cp, _sum, product = pokemon.all_stats(level/2.0, att_iv, def_iv, sta_iv)
            if cp <= max_cp:
                return (
                    level/2.0, att_iv, def_iv, sta_iv, cp, product,_sum
                )

    def get_combos(self, pokemon, max_cp):
        if pokemon.max_cp <= max_cp:
            yield (40, 15, 15, 15, pokemon.max_cp, pokemon.max_stat_product, pokemon.max_stat_sum)
            return
        combos = []
        for hp in reversed(range(0, 16)):
            for de in reversed(range(0, 16)):
                for at in reversed(range(0, 16)):
                    for lvl in reversed(range(20, 81)):
                        cp, _sum, prod = pokemon.all_stats(lvl/2.0, at, de, hp)
                        if cp <= max_cp:
                            combos.append((lvl/2.0, at, de, hp, cp, prod, _sum))
                            break
        combos.sort(key=lambda x: x[-1], reverse=True)
        for c in combos[0:50]:
            yield c

