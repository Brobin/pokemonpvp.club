import time

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property

from .utils import markdownify

from taggit.managers import TaggableManager


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=128, unique=True, editable=False)
    content = models.TextField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="articles", null=True, on_delete=models.DO_NOTHING)

    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    @cached_property
    def rendered_content(self):
        return markdownify(self.content)

    @cached_property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse('wiki-article', kwargs={'slug': self.slug})

    @cached_property
    def latest_edit(self):
        return self.edits.latest('created_at')

    class Meta:
        permissions = (
            ('editor', 'Can Add and edit wiki Articles'),
        )


class ArticleEdit(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="articles_edited", null=True, on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, related_name="edits", on_delete=models.CASCADE)
