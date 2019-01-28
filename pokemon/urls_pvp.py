from django.urls import path
from .views import PvpIVSpread


urlpatterns = [
    path('iv', PvpIVSpread.as_view(), name='pvp-iv'),
]
