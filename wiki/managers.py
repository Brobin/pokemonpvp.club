from django.db import models
from django.db.models import Q


class ArticleQuerySet(models.query.QuerySet):  # coverage: omit

    def visible_to(self, user):
        if user.has_perm('wiki.publisher'):
            return self.all()
        return self.filter(status=2)
