import mock

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.core.urlresolvers import reverse


from .utils import AdminUserTestCase, HTTP_OK
from ..models import Article


class AdminTestCase(AdminUserTestCase):
    TEST_DATA = {
        'title': 'Test',
        'content': 'Test',
        'edits-TOTAL_FORMS': '0',
        'edits-INITIAL_FORMS': '0',
        'edits-MIN_NUM_FORMS': '0',
        'edits-MAX_NUM_FORMS': '0',
    }

    def test_admin_article_index(self):
        url = reverse('admin:wiki_article_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_OK)

    @mock.patch('bulu.wiki.models.ArticleEdit.objects.create')
    def test_admin_article_create_post(self, edit_mock):
        url = reverse('admin:wiki_article_add')
        response = self.client.post(url, self.TEST_DATA)
        redirect = reverse('admin:wiki_article_changelist')
        self.assertRedirects(response, redirect)
        edit_mock.assert_called_once()
        self.assertEqual(Article.objects.count(), 1)

    @mock.patch('bulu.wiki.models.ArticleEdit.objects.create')
    def test_admin_article_edit_post(self, edit_mock):
        article = Article.objects.create(
            author=self.user,
            title='test',
            content='test'
        )
        url = reverse('admin:wiki_article_change', args=[article.id])
        response = self.client.post(url, self.TEST_DATA)
        redirect = reverse('admin:wiki_article_changelist')
        self.assertRedirects(response, redirect)
        edit_mock.assert_called_once()
        self.assertEqual(Article.objects.count(), 1)
