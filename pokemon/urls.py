from django.urls import path
from .views import PokemonView, PvpIVSpread


urlpatterns = [
    path('pvp', PvpIVSpread.as_view(), name='pvp'),
    path('', PokemonView.as_view(), name='pokemon'),
]
