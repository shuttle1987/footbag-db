from django.views.generic import ListView
from apps.footbagmoves.models import Component, Move

class ComponentList(ListView):
    """A list view for footbag components"""
    model = Component
    context_object_name = 'component_list'
    paginate_by = 15

class MoveList(ListView):
    """A list view for footbag moves"""
    model = Move
    context_object_name = 'move_list'
    paginate_by = 15
