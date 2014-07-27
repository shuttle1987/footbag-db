from django.db import models
#from django.utils.text import slugify
from django.template.defaultfilters import slugify

# a model for a footbag component
class Component(models.Model):
    """ A model for a footbag move component
    see https://github.com/shuttle1987/footbag-db/wiki/Abstract-model-for-footbag-moves
    and https://github.com/shuttle1987/footbag-db/wiki/Data-structure-implementation-for-footbag-moves
    """
    name = models.CharField(max_length=20)
    slug = models.SlugField(editable=False, unique=True)#editable=False hides slug from admin page

    def __unicode__(self):
        """ Unicode string representation of the object """
        return self.name

    def save(self, *args, **kwargs):
        """ Overriding the save method to generate a url slug"""
        if not self.id:
            #newly generated object as there is no DB key yet
            self.slug = slugify(self.name)
            super(Component, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """ Compute canonical URL for a Component object"""
        from django.core.urlresolvers import reverse
        #return reverse('apps.footbagmoves.components', args=[str(self.slug)])
        return reverse('apps.footbagmoves.components', args=[str(self.id)])

# a model for an entire footbag move
class Move(models.Model):
    """ A model for an entire footbag move 
    see https://github.com/shuttle1987/footbag-db/wiki/Abstract-model-for-footbag-moves
    and https://github.com/shuttle1987/footbag-db/wiki/Data-structure-implementation-for-footbag-moves
    """
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

