from django.contrib import admin

from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'team', 'xp',
        'great_veteran', 'ultra_veteran', 'master_veteran'
    ]
    list_display_links = ['id', 'name']
