import logging
import operator
import requests

from functools import reduce

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from pokemon.models import Pokemon
from pokemon.views import PvpIVSpread
from trainer.models import Trainer

from .serializers import PokemonSerializer, TrainerSerializer


log = logging.getLogger(__name__)


class MultipleFieldLookupMixin(object):

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filters = {
            field: self.kwargs[self.lookup_field]
            for field in self.lookup_fields
        }
        q = reduce(operator.or_, (Q(x) for x in filters.items()))
        return get_object_or_404(queryset, q)


class PokemonViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'list']
    queryset = Pokemon.objects.order_by('number')
    serializer_class = PokemonSerializer
    lookup_field = 'number'


class TrainerViewSet(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'list']
    queryset = Trainer.objects.order_by('id')
    serializer_class = TrainerSerializer
    lookup_field = 'name'
    lookup_fields = ('name', 'user__username')


class PokemonAPI(APIView):

    def get(self, request, name=None, number=None):
        if name:
            try:
                pokemon = Pokemon.objects.get(name__iexact=name.lower())
            except Pokemon.DoesNotExist:
                return Response(
                {'error': 'Pokemon Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if number:
            try:
                pokemon = Pokemon.objects.get(number=number)
            except Pokemon.DoesNotExist:
                return Response(
                {'error': 'Pokemon Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        number = pokemon.number
        base_url = 'https://db.pokemongohub.net/api/'
        data = requests.get('{0}/pokemon/{1}'.format(base_url, number)).json()
        data['moves'] = requests.get('{0}/moves/with-pokemon/{1}'.format(base_url, number)).json()
        return Response(data)


class PokemonMove(APIView):

    def get(self, request, name=None):
        url = 'https://db.pokemongohub.net/api/moves/with-filter/fast/with-stats'
        data = requests.get(url).json()
        name = name.replace('%20', ' ')
        for move in data:
            if name.lower() == move['name'].lower():
                return Response(move)
        url = 'https://db.pokemongohub.net/api/moves/with-filter/charge/with-stats'
        data = requests.get(url).json()
        name = name.replace('%20', ' ')
        for move in data:
            if name.lower() == move['name'].lower():
                return Response(move)
        return Response({'error': 'Move Not found'}, status=status.HTTP_404_NOT_FOUND)


class PvPIVAPI(PvpIVSpread, APIView):
    """
    list:
    Get a list of all 4096 IV combinations with ranking and stat product 
    for the specified pokemon and max CP.

    cp: Max CP of the pokemon (ie. 1500 or 2500)

    """

    def get(self, request, name, cp):
        try:
            pokemon = Pokemon.objects.get(name=name)
        except Pokemon.DoesNotExist:
            return Response(
                {'error': 'Pokemon Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if cp != 1500 and cp != 2500:
            return Response(
                {'error': 'CP must be 1500 or 2500'},
                status=status.HTTP_400_BAD_REQUEST
            )
        key = pokemon.name + str(cp)
        combos = cache.get(key)
        if not combos or settings.DEBUG:
            combos = list(self.get_combos(pokemon, cp, 0))
            cache.set(key, combos, 60*60*24*7)
        return Response({
            'pokemon': name,
            'max_cp': cp,
            'combos' :[{
                'rank': i+1,
                'level': c[0],
                'att_iv': c[1],
                'def_iv': c[2],
                'sta_iv': c[3],
                'att': c[4],
                'def': c[5],
                'sta': c[6],
                'cp': c[7],
                'stat_product': c[8],
                'stat_product_pct': c[9],
            } for i, c in enumerate(combos)]
        })
