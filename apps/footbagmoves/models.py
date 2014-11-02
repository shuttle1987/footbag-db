from django.db import models
from django.template.defaultfilters import slugify

from .video_assets_models import VideoAsset
from .video_api_helpers import extract_yt_id

from .constants import URL_VIDEO_TYPE, YOUTUBE_VIDEO_TYPE, VIDEO_TYPES

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
        return reverse('apps.footbagmoves.components', args=[str(self.id)])

class Move(models.Model):
    """ A model for organizing the information for an individual footbag move.
    Uses MoveComponentSequence to keep track of the squence of components that
    are contained in the move.
    see https://github.com/shuttle1987/footbag-db/wiki/Abstract-model-for-footbag-moves
    and https://github.com/shuttle1987/footbag-db/wiki/Data-structure-implementation-for-footbag-moves
    """
    name = models.CharField(max_length=40)
    slug = models.SlugField(editable=False, unique=True)#editable=False hides slug from admin page
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Overriding the save method to generate a url slug"""
        if not self.id:
            #newly generated object as there is no DB key yet
            self.slug = slugify(self.name)
            super(Move, self).save(*args, **kwargs)


class MoveComponentSequence(models.Model):
    """ This is essentially a table that keeps track of the sequences of components that
    are present in any given footbag move. We have to use use a table because the
    Django ORM doesn't deal with lists particularly well. """
    sequence_number = models.PositiveSmallIntegerField(default=0)
    component = models.ForeignKey(Component)
    move = models.ForeignKey(Move)

    def __unicode__(self):
        return u'%s, %d, %s' % (self.move.name, self.sequence_number, self.component.name)

class MoveDemonstrationVideo(VideoAsset):
    """ This is to keep track of move demonstration videos.
    Videos are stored as defined in VideoAsset and are associated with moves via this table."""
    move = models.ForeignKey(Move)

    def __unicode__(self):
        if self.use_start == True or self.use_end == True:
            return u'Demonstration video for Move: %s, %s, %s start: %d end %d' % (self.move.name, self.video_type, self.URL, self.start_time, self.end_time)
        else:
            return u'Demonstration video for Move: %s, %s, %s' % (self.move.name, self.video_type, self.URL)

class MoveTutorialVideo(VideoAsset):
    """ This is to keep track of move tutorial videos.
    Videos are stored as defined in VideoAsset and are associated with moves via this table."""
    move = models.ForeignKey(Move)

    def __unicode__(self):
        if self.use_start == True or self.use_end == True:
            return u'Tutorial video for Move: %s, %s, %s start: %d end %d' % (self.move.name, self.video_type, self.URL, self.start_time, self.end_time)
        else:
            return u'Tutorial video for Move: %s, %s, %s' % (self.move.name, self.video_type, self.URL)

class ComponentDemonstrationVideo(VideoAsset):
    """ This is to keep track of component demonstration videos.
    Videos are stored as defined in VideoAsset and are associated with components via this table."""
    component = models.ForeignKey(Component)

    def __unicode__(self):
        if self.use_start == True or self.use_end == True:
            return u'Demonstration video for Component: %s, %s, %s start: %d end %d' % (self.component.name, self.video_type, self.URL, self.start_time, self.end_time)
        else:
            return u'Demonstration video for Component: %s, %s, %s' % (self.component.name, self.video_type, self.URL)

class ComponentTutorialVideo(VideoAsset):
    """ This is to keep track of component tutorial videos.
    Videos are stored as defined in VideoAsset and are associated with components via this table."""
    component = models.ForeignKey(Component)

    def __unicode__(self):
        if self.use_start == True or self.use_end == True:
            return u'Tutorial video for Component: %s, %s, %s start: %d end %d' % (self.component.name, self.video_type, self.URL, self.start_time, self.end_time)
        else:
            return u'Tutorial video for Component: %s, %s, %s' % (self.component.name, self.video_type, self.URL)


class MoveNickname(models.Model):
    """Keep track of nicknames for footbag moves."""
    move = models.ForeignKey(Move)
    nickname = models.CharField(max_length=40, unique=True)
    rating = models.SmallIntegerField(default=0)

class ComponentNickname(models.Model):
    """Keep track of nicknames for footbag components."""
    move = models.ForeignKey(Component)
    nickname = models.CharField(max_length=40, unique=True)
    rating = models.SmallIntegerField(default=0)
