from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Article
from ..search_indexes import ArticleIndex


class ArticleIndexTestCase(TestCase):

    def test_prepare_tags(self):
        article = Article.objects.create(
            title='test',
            author=get_user_model().objects.create_superuser(
                username='test@test.com',
                email='test@test.com',
                password='Pank8888'
            ),
            content="<table>"
        )
        article.tags.add("test")
        article.tags.add("dev")
        index = ArticleIndex()
        result = index.prepare_tags(article)
        self.assertEqual(result, 'test dev')
