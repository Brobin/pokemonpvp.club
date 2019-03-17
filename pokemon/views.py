from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from math import floor

from .models import Pokemon, Type


class PokemonBaseStats(ListView):
    template_name = 'pokemon/base_stats.html'
    queryset = Pokemon.objects.order_by('number')


class PokemonList(ListView):
    template_name = 'pokemon/list.html'
    queryset = Pokemon.objects.order_by('number')


class PokemonDetail(DetailView):
    template_name = 'pokemon/detail.html'
    model = Pokemon
    slug_field = 'number'
    slug_url_kwarg = 'number'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['types'] = Type.objects.order_by('name')
        return context


class TypeMatchupsView(ListView):
    template_name = 'pokemon/type_matchups.html'
    queryset = Type.objects.order_by('name')


class PvpIVSpread(TemplateView):
    template_name = 'pokemon/pvp/iv_spread.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['choices'] = Pokemon.objects.order_by('name')
        
        pokemon = self.request.GET.get('pokemon', 'Skarmory')
        max_cp = int(self.request.GET.get('max_cp', 1500))
        min_iv = int(self.request.GET.get('min_iv', 0))

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
        context['min_iv'] = min_iv

        if min_iv == 0:
            key = pokemon.name + str(max_cp)
        else:
            key = '{0}{1}-{2}'.format(pokemon.name, max_cp, min_iv)
        combos = cache.get(key)
        if not combos or settings.DEBUG:
            combos = list(self.get_combos(pokemon, max_cp, min_iv))
            cache.set(key, combos, 60*60*24*7)
        context['num_combos'] = len(combos)
        context['combos'] = combos[0:25]
        max_product = combos[0][-2]
        context['my_combo'] = self.get_my_combo(
            pokemon, context['att_iv'], context['def_iv'],
            context['sta_iv'], max_cp, max_product)
        try:
            context['rank'] = combos.index(context['my_combo']) + 1
        except:
            context['rank'] = 'Not Found'
        return context

    def get_my_combo(self, pokemon, att_iv, def_iv, sta_iv, max_cp, max_product):
        for level in reversed(range(20, 81)):
            cp, a, d, s, product = pokemon.all_stats(level/2.0, att_iv, def_iv, sta_iv)
            if cp <= max_cp:
                return (
                    level/2.0, att_iv, def_iv, sta_iv, a, d, s, cp, product, product / max_product * 100
                )

    def get_combos(self, pokemon, max_cp, min_iv):
        combos = []
        for hp in reversed(range(min_iv, 16)):
            for de in reversed(range(min_iv, 16)):
                for at in reversed(range(min_iv, 16)):
                    for lvl in reversed(range(20, 81)):
                        cp, a, d, s, prod = pokemon.all_stats(lvl/2.0, at, de, hp)
                        if cp <= max_cp:
                            combos.append((lvl/2.0, at, de, hp, a, d, s, cp, prod))
                            break
        combos.sort(key=lambda x: x[-1], reverse=True)
        _max = combos[0][-1]
        for c in combos:
            yield c + (c[-1]/_max *100.0,)
