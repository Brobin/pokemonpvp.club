from django.contrib import admin

from .models import Cache

@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ['cache_key', 'expires']
    search_fields = ['cache_key']
    readonly_fields = ['cache_key', 'value']
