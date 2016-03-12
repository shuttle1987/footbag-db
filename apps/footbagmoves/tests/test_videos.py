from django.test import TestCase
from apps.footbagmoves.video_api_helpers import extract_yt_id
from apps.footbagmoves.forms import VideoEntryForm
from apps.footbagmoves.models import YOUTUBE_VIDEO_TYPE, URL_VIDEO_TYPE

from apps.footbagmoves.edit_views import MoveDemoVideoFormset

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

class TestVideoFormset(TestCase):
    """Test the video formset functionality"""

    def setUp(self):
        from apps.footbagmoves.models import Move
        self.move = Move(name="test move")
        self.move.save()

    def form_data(self, video_0, video_1):
        data = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 0,
            'form-MAM_NUM_FORMS': 15,
            'form-0-video_type': video_0["type"],
            'form-0-URL': video_0["URL"],
            'form-0-start_time': video_0["start_time"],
            'form-0-end_time': video_0["end_time"],
            'form-0-move': self.move,
            'form-1-video_type': video_1["type"],
            'form-1-URL': video_1["URL"],
            'form-1-start_time': video_1["start_time"],
            'form-1-end_time': video_1["end_time"],
            'form-1-move': self.move,
        }
        return MoveDemoVideoFormset(
            data,
            instance = self.move,
            prefix = 'form'
        )

    def test_duplicate_videos(self):
        """Test duplicate videos fail validation"""
        video_0 = {
            "type": YOUTUBE_VIDEO_TYPE,
            "URL": 'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            "start_time": 0,
            "end_time": 0,
        }

        video_1 = {
            "type": YOUTUBE_VIDEO_TYPE,
            "URL": 'http://www.youtube.com/watch?v=DJ_uZiueQKg',
            "start_time": 0,
            "end_time": 0,
        }

        form = self.form_data(video_0, video_1)
        self.assertFalse(form.is_valid())
