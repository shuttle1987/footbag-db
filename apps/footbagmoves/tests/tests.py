from django.test import TestCase

from apps.footbagmoves.models import Component, Move, MoveComponentSequence

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

        #Test the component saved its name properly in the DB
        self.assertEquals(only_component_in_db.name, "Toe stall")
        self.assertEquals(str(comp1), "Toe stall")

class MoveCreationTest(TestCase):
    """Tests for creating footbag moves"""

    def setUp(self):
        """Set up components for use with Move tests"""
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
        #Test the move saved its name properly in the DB
        self.assertEquals(only_move_in_db.name, "Toe kick")


from apps.footbagmoves.edit_views import ComponentSequenceFormset
class MoveComponentSequences(TestCase):
    """Tests for the move component sequences"""
    
    def setUp(self):
        self.component_toe_kick = Component(name="Toe kick")
        self.component_toe_kick.save()
        self.test_move = Move(name='test move')
        self.test_move.save()

    def form_data(self, move, component0_id, component0_seq_number, component1_id, component1_seq_number):
        data = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 0,
            'form-MAM_NUM_FORMS': 15,
            'form-0-sequence_number': component0_seq_number,
            'form-0-component': component0_id,
            'form-1-sequence_number': component1_seq_number,
            'form-1-component': component1_id,
        }
        return ComponentSequenceFormset(
            data,
            instance = move,
            prefix = 'form'
        )

    def test_valid_data(self):
        """Test that a valid move passes validation"""
        form = self.form_data(
            self.test_move,
            self.component_toe_kick.id,
            0,
            self.component_toe_kick.id,
            1
        )
        self.assertTrue(form.is_valid())

    def test_duplicated_sequence(self):
        """Test that a move with duplicated sequence fails validation"""
        form = self.form_data(
            self.test_move,
            self.component_toe_kick.id,
            0,
            self.component_toe_kick.id,
            0
        )
        self.assertFalse(form.is_valid())

    def test_invalid_sequence_number(self):
        """Test that a move with invalid sequence fails validation"""
        form = self.form_data(
            self.test_move,
            self.component_toe_kick.id,
            -1,
            self.component_toe_kick.id,
            0
        )
        self.assertFalse(form.is_valid())

    def test_missing_sequence_number(self):
        """Test that a move with missing sequence fails validation"""
        form = self.form_data(
            self.test_move,
            self.component_toe_kick.id,
            "",
            self.component_toe_kick.id,
            1
        )
        self.assertFalse(form.is_valid())
