import datetime
from haystack import indexes
from market.apps.models import App


class AppIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr="name")
    text = indexes.CharField(document=True, use_template=True, model_attr='description')
    homepage = indexes.CharField(model_attr="homepage")
    uploader = indexes.CharField(model_attr='uploader')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return App

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
