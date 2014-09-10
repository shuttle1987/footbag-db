from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from apps.footbagmoves.models import Component, Move, MoveComponentSequence
from apps.footbagmoves.models import ComponentTutorialVideo, ComponentDemonstrationVideo
from apps.footbagmoves.models import MoveTutorialVideo, MoveDemonstrationVideo

from apps.footbagmoves.forms import VideoEntryForm


class VideosFormset(BaseInlineFormSet):
    """A set of video entry forms """
    def is_valid(self):
        return (super(VideosFormset,self).is_valid() and
                not any(bool(e) for e in self.errors))

    def clean(self):
        super(VideosFormset, self).clean()
        for form in self.forms:
            form.is_valid()

class VideoEntryAdmin(admin.TabularInline):
    """ Single video entry """
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

class MoveAdmin(admin.ModelAdmin): 
    """Admin helper for the moves """
    inlines = (
            MoveComponentSequenceInline,
            MoveDemonstrationVideoInline,
            MoveTutorialVideoInline,
    )


admin.site.register(Component, ComponentAdmin)
admin.site.register(Move, MoveAdmin)
