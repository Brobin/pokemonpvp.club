from django.urls import path
from .views import BestPokemon, PvpIVSpread


urlpatterns = [
    path('best', BestPokemon.as_view(), name='pvp-best'),
    path('iv', PvpIVSpread.as_view(), name='pvp-iv'),
]
