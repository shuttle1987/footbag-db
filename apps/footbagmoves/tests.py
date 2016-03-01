from django.test import TestCase

from apps.footbagmoves.video_api_helpers import extract_yt_id
from apps.footbagmoves.models import Component, YOUTUBE_VIDEO_TYPE
from apps.footbagmoves.forms import VideoEntryForm

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

class ComponentCreationTest(TestCase):
    """Test that we can successfully create a component"""
    def test_creating_component_and_saving_to_db(self):
        """Test that we can create a component and save it to the database"""
        comp1 = Component()
        comp1.name = "Toe stall"
        comp1.save()

        all_components_in_db = Component.objects.all()
        self.assertEquals(len(all_components_in_db), 1)
        only_component_in_db = all_components_in_db[0]
        self.assertEquals(only_component_in_db, comp1)

        #Test the component saved it's name properly in the DB
        self.assertEquals(only_component_in_db.name, "Toe stall")
