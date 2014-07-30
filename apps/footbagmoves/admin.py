from django.contrib import admin
from apps.footbagmoves.models import Component, Move, MoveComponentSequence

class MoveComponentSequenceInline(admin.TabularInline):
    """ Inline admin for the move sequences. This is so we can edit the components
    sequence in the same place in the Admin page as the moves"""
    model = MoveComponentSequence

class MoveAdmin(admin.ModelAdmin): 
    """Admin helper for the moves """
    inlines = [
            MoveComponentSequenceInline,
    ]

admin.site.register(Component)
admin.site.register(Move, MoveAdmin)
