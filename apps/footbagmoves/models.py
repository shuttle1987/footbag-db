from django.db import models

# a model for a footbag component
class Component(models.Model):
    """ A model for a footbag move component
    see https://github.com/shuttle1987/footbag-db/wiki/Abstract-model-for-footbag-moves
    and https://github.com/shuttle1987/footbag-db/wiki/Data-structure-implementation-for-footbag-moves
    """
    name = model.CharField(max_length=20)
    def __unicode__(self):
        return self.name

# a model for an entire footbag move
class Component(models.Model):
    """ A model for an entire footbag move 
    see https://github.com/shuttle1987/footbag-db/wiki/Abstract-model-for-footbag-moves
    and https://github.com/shuttle1987/footbag-db/wiki/Data-structure-implementation-for-footbag-moves
    """
    name = model.CharField(max_length=30)
    def __unicode__(self):
        return self.name

