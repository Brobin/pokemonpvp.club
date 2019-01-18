from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PokemonView, PvpIVSpread


urlpatterns = [
    path('pvp', PvpIVSpread.as_view(), name='pvp'),
    path('', cache_page(60*60*24)(PokemonView.as_view()), name='pokemon'),
]
