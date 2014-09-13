from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from apps.footbagmoves.models import Component, Move, MoveComponentSequence
from apps.footbagmoves.models import ComponentTutorialVideo, ComponentDemonstrationVideo
from apps.footbagmoves.models import MoveTutorialVideo, MoveDemonstrationVideo

from apps.footbagmoves.forms import VideosFormset, VideoEntryForm, AtLeastOneRequiredInlineFormset


class VideoEntryAdmin(admin.TabularInline):
    """ Single video entry """
    #TODO: remove this?
    pass

class ComponentDemonstrationVideoInline(admin.TabularInline):
    """Inline admin to link to a demonstation video for a component"""
    model = ComponentDemonstrationVideo

class ComponentTutorialVideoInline(admin.TabularInline):
    """Inline admin to link to a tutorial video for a component"""
    model = ComponentTutorialVideo

class ComponentAdmin(admin.ModelAdmin):
    """Admin helper for the components"""
    fields = ('name',)
    inlines = (
            ComponentDemonstrationVideoInline,
            ComponentTutorialVideoInline,
    )


class MoveDemonstrationVideoInline(admin.TabularInline):
    """Inline admin to link to a demonstation video for a Move"""
    model = MoveDemonstrationVideo
    form = VideoEntryForm
    formset = VideosFormset

class MoveTutorialVideoInline(admin.TabularInline):
    """Inline admin to link to a tutorial video for a Move"""
    model = MoveTutorialVideo

class MoveComponentSequenceInline(admin.TabularInline):
    """ Inline admin for the move sequences. This is so we can edit the components
    sequence in the same place in the Admin page as the moves"""
    model = MoveComponentSequence
    formset = AtLeastOneRequiredInlineFormset

class MoveAdmin(admin.ModelAdmin): 
    """Admin helper for the moves """
    inlines = (
            MoveComponentSequenceInline,
            MoveDemonstrationVideoInline,
            MoveTutorialVideoInline,
    )


admin.site.register(Component, ComponentAdmin)
admin.site.register(Move, MoveAdmin)
