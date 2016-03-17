"""Indexing for the footbagmoves models for use with Haystack search"""
from haystack import indexes
from apps.footbagmoves.models import Component, Move


class ComponentIndex(indexes.SearchIndex, indexes.Indexable):
    """Search indexing for the footbag Component objects"""
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Component

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class MoveIndex(indexes.SearchIndex, indexes.Indexable):
    """Search indexing for the footbag Move objects"""
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Move

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
