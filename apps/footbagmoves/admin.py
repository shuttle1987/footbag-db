from django.contrib import admin
from apps.footbagmoves.models import Component, Move, MoveComponentSequence
from apps.footbagmoves.models import ComponentTutorialVideo, ComponentDemonstrationVideo

class ComponentDemonstrationVideoInline(admin.TabularInline):
    """Inline admin to link to a demonstation video for a component"""
    model = ComponentDemonstrationVideo

class ComponentTutorialVideoInline(admin.TabularInline):
    """Inline admin to link to a tutorial video for a component"""
    model = ComponentTutorialVideo

class ComponentAdmin(admin.ModelAdmin):
    """Admin helper for the components"""
    fields = ('name',)
    inlines = [
            ComponentDemonstrationVideoInline,
            ComponentTutorialVideoInline,
    ]

class MoveComponentSequenceInline(admin.TabularInline):
    """ Inline admin for the move sequences. This is so we can edit the components
    sequence in the same place in the Admin page as the moves"""
    model = MoveComponentSequence

class MoveAdmin(admin.ModelAdmin): 
    """Admin helper for the moves """
    inlines = [
            MoveComponentSequenceInline,
    ]

admin.site.register(Component, ComponentAdmin)
admin.site.register(Move, MoveAdmin)
