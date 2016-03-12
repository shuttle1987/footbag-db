from django.test import TestCase
from apps.footbagmoves.video_api_helpers import extract_yt_id
from apps.footbagmoves.forms import VideoEntryForm
from apps.footbagmoves.models import YOUTUBE_VIDEO_TYPE, URL_VIDEO_TYPE

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

    def form_data(selfi, vid_type, url, use_end, use_start, start_time, end_time):
        return VideoEntryForm(data = {
            'video_type': vid_type,
            'URL': url,
            'use_end': use_end,
            'use_start': use_start,
            'start_time': start_time,
            'end_time': end_time,
        })

    def test_invalid_start_end_times(self):
        """Test that a start time occuring after an end time fails validation"""
        form = self.form_data(
            YOUTUBE_VIDEO_TYPE,
            'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            True,
            True,
            15,
            5,
        )
        self.assertFalse(form.is_valid())

    def test_valid_youtube_video(self):
        """Test that a valid youtube video passes the validation """
        form = self.form_data(
            YOUTUBE_VIDEO_TYPE,
            'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            'on',
            'on',
            5,
            15,
        )
        self.assertTrue(form.is_valid())

    def test_enter_youtube_as_URL(self):
        """Make sure that youtube video fails validation when classified as URL type"""
        form = self.form_data(
            URL_VIDEO_TYPE,
            'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            'on',
            'on',
            5,
            15,
        )
        self.assertFalse(form.is_valid())
