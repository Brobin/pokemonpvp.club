from django.contrib import admin
from django.db import models

from markdownx.widgets import AdminMarkdownxWidget

from .models import Article, ArticleEdit


class ArtcleEditInline(admin.TabularInline):
    model = ArticleEdit
    readonly_fields = ['created_at', 'editor']
    can_add = False
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at', 'status']
    list_display_links = ['title']
    fields = ['title', 'tags', 'pokemon', 'content']
    inlines = [ArtcleEditInline]
    actions = ['publish', 'set_to_draft']

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

    def publish(self, request, queryset):
        queryset.update(status=Article.PUBLISHED)
    publish.short_description = 'Publish Articles'

    def set_to_draft(self, request, queryset):
        queryset.update(status=Article.DRAFT)
    set_to_draft.short_description = 'Set to Draft'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        obj.save()
        ArticleEdit.objects.create(
            editor=request.user,
            article=obj
        )
