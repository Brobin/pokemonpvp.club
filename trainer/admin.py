from django.contrib import admin

from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'user', 'team', 'xp',
        'great_veteran', 'ultra_veteran', 'master_veteran'
    ]
    list_display_links = ['id', 'name',  'user']
    list_filter = ['team']
    search_fields = ['name', 'user__username']
    readonly_fields = ['user']
    fieldsets = (
        ('Trainer Info', {
            'fields': ['user', 'name', 'team', 'xp']
        }),
        ('Pokedex', {
            'fields': ['kanto', 'johto', 'hoenn', 'sinnoh']
        }),
        ('PvP', {
            'classes': ('inline',),
            'fields': ['great_veteran', 'ultra_veteran', 'master_veteran']
        }),
        ('Achievements', {
            'classes': ('collapse',),
            'fields': [
                'jogger', 'collector', 'breeder', 'scientist',
                'backpacker', 'battle_girl', 'youngster',
                'pikachu_fan','berry_master', 'gym_leader',
                'pokemon_ranger', 'idol', 'gentleman', 'pilot', 'fisherman',
                'ace_trainer',  'unown', 'champion', 'battle_legend'
            ]
        }),
        ('Type Medals', {
            'classes': ('collapse',),
            'fields': [
                'schoolkid', 'black_belt', 'bird_keepr', 'punk_girl',
                'ruin_maniac', 'hiker', 'bug_catcher', 'hex_maniac',
                'depot_agent', 'kindler', 'swimmer', 'gardener', 'rocker',
                'psychic', 'skier', 'dragon_tamer', 'delinquent', 'fairy_tale_girl'
            ]
        })
    )