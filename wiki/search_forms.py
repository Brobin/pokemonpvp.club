import logging

from haystack.backends import SQ
from haystack.inputs import AutoQuery
from haystack.forms import SearchForm

from .models import Article


log = logging.getLogger(__name__)


class ArticleSearchForm(SearchForm):
    models = [Article]

    def get_models(self):
        return self.models

    def search(self):
        """Override the base search method for our custom filtering."""
        if not self.is_valid():
            log.error("Not valid!!!")
            return self.no_query_found()
        q = self.cleaned_data['q']
        # Join the query with the text and title so our weight is applied
        query = SQ(text=AutoQuery(q)) | SQ(title=AutoQuery(q))
        # Filter out the querysey with our query and the Product model
        return self.searchqueryset.filter(query).models(*self.get_models())
