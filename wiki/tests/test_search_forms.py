import mock

from django.test import TestCase

from ..models import Article
from ..search_forms import ArticleSearchForm


class ArticleSearchFormTestCase(TestCase):

    def setUp(self):
        super(ArticleSearchFormTestCase, self).setUp()
        self.form = ArticleSearchForm()

    def test_get_models(self):
        self.assertEqual(self.form.get_models(), [Article])

    def test_no_query_found(self):
        self.assertEqual(self.form.no_query_found().count(), 0)

    @mock.patch('bulu.wiki.search_forms.log.error')
    def test_invalid(self, log_mock):
        result = self.form.search()
        self.assertEqual(self.form.no_query_found().count(), result.count())
        log_mock.assert_called_once()
