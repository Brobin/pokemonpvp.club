from django.contrib import admin

from .models import Type, Pokemon


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


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
