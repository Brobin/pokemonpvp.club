from django.db import models
from django.db.models import F


class TrainerManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(pokedex_entries=F('kanto')+F('johto')+F('hoenn')+F('sinnoh'))
