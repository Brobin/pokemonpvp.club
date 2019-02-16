from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Article


class ModelTestCase(TestCase):

    def create_test_article(self):
        return Article.objects.create(
            title='test',
            author=get_user_model().objects.create_superuser(
                username='test@test.com',
                email='test@test.com',
                password='Pank8888'
            ),
            content="<table>"
        )

    def test_article_rendered_content(self):
        article = self.create_test_article()
        self.assertEqual(
            article.rendered_content,
            '<table class="table table-striped table-hover">'
        )

    def test_article_url(self):
        article = self.create_test_article()
        expect = reverse('wiki-article', kwargs={'slug': article.slug})
        self.assertEqual(article.url, expect)
