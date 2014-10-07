from django.views.generic import ListView
from apps.footbagmoves.models import Move

class MoveList(ListView):
    """A list view for footbag moves"""
    model = Move
    context_object_name = 'move_list'
    paginate_by = 15
