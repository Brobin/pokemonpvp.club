from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from .views import PokemonView, TypeMatchupsView, PvpIVSpread


urlpatterns = [
    path('types', TypeMatchupsView.as_view(), name='pokemon-types'),
    path('pvp', RedirectView.as_view(url=reverse_lazy('pvp-iv'))),
    path('', PokemonView.as_view(), name='pokemon-stats'),
]
