from django.urls import path
from .views import PokemonView, TypeMatchupsView, PvpIVSpread


urlpatterns = [
    path('types', TypeMatchupsView.as_view(), name='types'),
    path('pvp', PvpIVSpread.as_view(), name='pvp'),
    path('', PokemonView.as_view(), name='pokemon'),
]
