from django.contrib import admin

from .models import Type, TypeMatchup, Pokemon, SilphCup


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(TypeMatchup)
class TypeMatchupAdmin(admin.ModelAdmin):
    list_display = ['attacking_type', 'defending_type', 'multiplier']


@admin.register(SilphCup)
class SilphCupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = [
        'number', 'name', 'base_attack', 'base_defense',
        'base_stamina', 'primary_type', 'secondary_type'
    ]
    list_display_links = ['number', 'name']
    search_fields = ['name']
    list_filter = ['primary_type', 'secondary_type']
    ordering = ('number',)
