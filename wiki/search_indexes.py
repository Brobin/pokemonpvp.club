from haystack import indexes

from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    updated_at = indexes.DateTimeField(model_attr='updated_at')
    title = indexes.CharField(model_attr='title', boost=1.25)
    tags = indexes.CharField(boost=1.25)

    name_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Article

    def prepare_tags(self, obj):
        return " ".join([t.name for t in obj.tags.all()])
