from django.test import TestCase

from apps.footbagmoves.video_api_helpers import extract_yt_id
from apps.footbagmoves.models import Component, Move, MoveComponentSequence, YOUTUBE_VIDEO_TYPE
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

class MoveCreationTest(TestCase):
    """Tests for creating footbag moves"""

    def setUp(self):
        """Set up components for use wiht Move tests"""
        self.component_toe_kick = Component(name="Toe kick")
        self.component_toe_kick.save()

    def test_creating_move(self):
        """Test we can create a move and save it"""
        move_toe_kick = Move(name="Toe kick")
        move_toe_kick.save()
        component_sequence = MoveComponentSequence(
            sequence_number=0,
            component=self.component_toe_kick,
            move=move_toe_kick
        )
        component_sequence.save()

        all_moves_in_db = Move.objects.all()
        self.assertEquals(len(all_moves_in_db), 1)
        only_move_in_db = all_moves_in_db[0]
        self.assertEquals(only_move_in_db, move_toe_kick)
        #Test the component saved it's name properly in the DB
        self.assertEquals(only_move_in_db.name, "Toe kick")

    def duplicate_component_should_fail_validation(self):
        """
        Test that a move with more than one component with the same sequence
        number should fail validation
        """
        pass


from .edit_views import ComponentSequenceFormset
class MoveComponentSequences(TestCase):
    """Tests for the move component sequences"""
    
    def setUp(self):
        self.component_toe_kick = Component(name="Toe kick")
        self.component_toe_kick.save()

    def form_data(self, move, component0_name, component0_seq_number, component1_name, component1_seq_number):
        return ComponentSequenceFormset(
            move = move,
            data = {
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAM_NUM_FORMS': 15,
                'form-0-sequence-number': component0_seq_number,
                'form-0-component': component0_name,
                'form-1-sequence-number': component1_seq_number,
                'form-1-component': component1_name,
            }
        )

    def test_valid_data(self):
        move = Move(name="Toe kick")
        form = self.form_data(
            move,
            self.component_toe_kick.name,
            0,
            self.component_toe_kick.name,
            1
        )
