from haystack import indexes

from providerbackend.models import ProviderMetaData
from providerbackend.models import Job


class ProviderMetaDataIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ProviderMetaData

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class JobIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Job

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
