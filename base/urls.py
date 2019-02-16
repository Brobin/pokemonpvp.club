from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from leaderboard.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('allauth.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('pokemon/', include('pokemon.urls')),
    path('pvp/', include('pokemon.urls_pvp')),
    path('trainer/', include('trainer.urls')),
    path('legal/', TemplateView.as_view(template_name='legal.html'), name='legal'),
    path('wiki/', include('wiki.urls')),
    path('', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
