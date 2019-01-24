from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from .views import (
    PokemonBaseStats,
    PokemonList,
    PokemonDetail,
    TypeMatchupsView
)


urlpatterns = [
    path('types', TypeMatchupsView.as_view(), name='pokemon-types'),
    path('pvp', RedirectView.as_view(url=reverse_lazy('pvp-iv'))),
    path('<int:number>', PokemonDetail.as_view(), name='pokemon-detail'),
    path('stats', PokemonBaseStats.as_view(), name='pokemon-stats'),
    path('', PokemonList.as_view(), name='pokemon-list'),
]
