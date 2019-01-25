import uuid

from django.db import models


class Cache(models.Model):
    cache_key = models.CharField(max_length=255, primary_key=True)
    value = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        verbose_name = 'Cache Object'
        verbose_name_plural = 'Cache Objects'
        db_table = 'cache'


class BaseModel(models.Model):
    """BaseModel
    Base model that handles ids, uuid, and both the created_at
    and updated_at fields. Add methods here that all models in
    the project will share. This is an abstract model, all models
    in the project should extend it.
    """
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    DATE_FORMAT = '{0:%m/%d/%Y, %-I:%M %p}'

    def save(self, *args, **kwargs):
        """Overrides the save method to update the created_at and
        updated_at timestamps.
        """
        from django.utils import timezone
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    @property
    def created(self):  # coverage: omit
        """Formatted created_at timestamp"""
        return self.DATE_FORMAT.format(self.created_at)

    @property
    def updated(self):  # coverage: omit
        """Formatted updated_at timestamp"""
        return self.DATE_FORMAT.format(self.updated_at)

    class Meta:
        abstract = True