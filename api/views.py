import logging

from django.conf import settings
from django.core.cache import cache
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


class PokemonViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'list']
    queryset = Pokemon.objects.order_by('number')
    serializer_class = PokemonSerializer
    lookup_field = 'number'


class TrainerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'list']
    queryset = Trainer.objects.order_by('id')
    serializer_class = TrainerSerializer
    lookup_field = 'name'


class TrainerUsernameViewSet(TrainerViewSet):
    lookup_field = 'user__username'


class PvPIVAPI(PvpIVSpread, APIView):
    """
    list:
    Get a list of all 4096 IV combinations with ranking and stat product 
    for the specified pokemon and max CP.
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
            combos = list(self.get_combos(pokemon, cp))
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
