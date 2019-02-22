from django.conf import settings
from django.urls import include, path

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register('pokemon', views.PokemonViewSet, 'api-pokemon')
router.register('trainers', views.TrainerViewSet, 'api-trainers')

urlpatterns = [
    path('pokemon-detail/<int:number>/', views.PokemonAPI.as_view(), name='pokemon-nubmer'),
    path('pokemon-detail/<str:name>/', views.PokemonAPI.as_view(), name='pokemon-name'),
    path('pvp/iv/<str:name>/<int:cp>', views.PvPIVAPI.as_view(), name='pvp-iv-api'),
    path('docs', include_docs_urls(title='Pokemon PvP Club API')),
    path('', include(router.urls))
]
