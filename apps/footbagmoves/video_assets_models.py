"""Video assets as used in this project are stored as VideoAsset.
Any model that uses a video should either inherit from VideoAsset or have a foreign
key to a VideoAsset"""

from django.db import models

from video_api_helpers import extract_yt_id
from constants import URL_VIDEO_TYPE, YOUTUBE_VIDEO_TYPE, VIDEO_TYPES

class VideoAsset(models.Model):
    """This is a video asset, specifies the type of the video along with it's location
    and stores some other information about the timestamps for the relevant parts of the video."""
    video_type = models.CharField(max_length=1, choices=VIDEO_TYPES, default=URL_VIDEO_TYPE)
    URL = models.URLField()
    video_id = models.CharField(max_length=20)
    use_start = models.BooleanField(default=False)
    start_time = models.PositiveSmallIntegerField()
    use_end = models.BooleanField(default=False)
    end_time = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        """Overriding the save for youtube videos to store ID internally"""
        if(self.video_type == YOUTUBE_VIDEO_TYPE):
            self.video_id = extract_yt_id(self.URL)
        super(VideoAsset, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.use_start == True or self.use_end == True:
            return u'Video: %s, %s start: %d end %d' % (self.URL, self.video_type, self.start_time, self.end_time)
        else:
            return u'Video: %s, %s' % (self.URL, self.video_type)

