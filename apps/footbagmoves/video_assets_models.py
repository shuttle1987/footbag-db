"""Video assets as used in this project are stored as VideoAsset.
Any model that uses a video should either inherit from VideoAsset or have a foreign
key to a VideoAsset"""

from django.db import models

from .video_api_helpers import extract_yt_id
from .constants import URL_VIDEO_TYPE, YOUTUBE_VIDEO_TYPE, VIDEO_TYPES

class VideoAsset(models.Model):
    """This is a video asset, specifies the type of the video along with it's location
    and stores some other information about the timestamps for the relevant parts of the video."""
    video_type = models.CharField(max_length=1, choices=VIDEO_TYPES, default=URL_VIDEO_TYPE)
    URL = models.URLField()
    video_id = models.CharField(max_length=20)
    use_start = models.BooleanField(default=False)
    start_time = models.PositiveSmallIntegerField(default=0)
    use_end = models.BooleanField(default=False)
    end_time = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        """In order to correctly create instances of VideoAsset we need to override the save method.
        The start and end times when defined by `start_time` and `end_time` in the forms have to set
        `use_start` and `use_end` upon saving to the database.
        We also need to extract the ID from youtube videos to store internally"""
        if self.video_type == YOUTUBE_VIDEO_TYPE:
            self.video_id = extract_yt_id(self.URL)

        if self.start_time:
            self.use_start = True
        else:
            self.use_start = False
            self.start_time = 0

        if self.end_time:
            self.use_end = True
        else:
            self.use_end = False
            self.end_time = 0
        super(VideoAsset, self).save(*args, **kwargs)

    def __str__(self):
        if self.use_start == True or self.use_end == True:
            return 'Video: %s, %s start: %d end %d' % (self.URL,
                                                       self.video_type,
                                                       self.start_time,
                                                       self.end_time)
        else:
            return 'Video: %s, %s' % (self.URL, self.video_type)

