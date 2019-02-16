from django.core.urlresolvers import reverse

from .utils import AdminUserTestCase, HTTP_OK
from ..models import Article


class ViewsTestCase(AdminUserTestCase):

    def test_wiki_index(self):
        url = reverse('wiki-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_wiki_search(self):
        url = reverse('wiki-search') + '?q=test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_wiki_tag(self):
        article = Article.objects.create(
            title='test',
            content='tests',
            author=self.user,
        )
        article.tags.add('test')
        url = reverse('wiki-tag', kwargs={'slug': 'test'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_wiki_article(self):
        article = Article.objects.create(
            title='test',
            content='tests',
            author=self.user,
        )
        url = reverse('wiki-article', kwargs={'slug': article.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_wiki_article_404(self):
        slug = 'test2'
        url = reverse('wiki-article', kwargs={'slug': slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, slug.title())
