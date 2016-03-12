from django.test import TestCase
from apps.footbagmoves.video_api_helpers import extract_yt_id
from apps.footbagmoves.forms import VideoEntryForm
from apps.footbagmoves.models import YOUTUBE_VIDEO_TYPE

class YoutubeIDExtraction(TestCase):
    """Test functionality that extracts the youtube ID from a youtube URL"""

    def test_extract_youtube_id(self):
        """Tests that the ID gets extracted from a full youtube URL correctly """
        self.assertEqual(extract_yt_id("http://www.youtube.com/watch?v=L-ZBwq9wW_s"), "L-ZBwq9wW_s")
        self.assertEqual(extract_yt_id("https://www.youtube.com/watch?v=L-ZBwq9wW_s"), "L-ZBwq9wW_s")
        self.assertEqual(extract_yt_id("http://youtube.com/watch?v=L-ZBwq9wW_s"), "L-ZBwq9wW_s")
        self.assertEqual(extract_yt_id("https://youtube.com/watch?v=L-ZBwq9wW_s"), "L-ZBwq9wW_s")
        self.assertEqual(extract_yt_id("http://youtu.be/kiBZbcvGrZI"), "kiBZbcvGrZI")

class VideoEntryFormTests(TestCase):
    """Test video entry from forms validation"""
    def test_invalid_start_end_times(self):
        """Test that a start time occuring after an end time fails validation"""
        form_data = {
            'video_type': YOUTUBE_VIDEO_TYPE,
            'URL': 'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            'use_end': True,
            'use_start': True,
            'start_time': 15,
            'end_time': 5,
        }
        form = VideoEntryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_youtube_video(self):
        """Test that a valid youtube video passes the validation """
        form_data = {
            'video_type': YOUTUBE_VIDEO_TYPE,
            'URL': 'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            'use_end': 'on',
            'use_start': 'on',
            'start_time': 5,
            'end_time': 15,
        }
        form = VideoEntryForm(data=form_data)
        self.assertTrue(form.is_valid())
