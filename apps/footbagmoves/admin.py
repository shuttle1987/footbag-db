from django.contrib import admin

from apps.footbagmoves.models import (
    Component, Move, MoveComponentSequence,
    ComponentTutorialVideo, ComponentDemonstrationVideo,
    MoveTutorialVideo, MoveDemonstrationVideo,
    ComponentNickname, MoveNickname,
    ComponentTips, MoveTips,
)

from apps.footbagmoves.forms import (
    VideosFormset,
    VideoEntryForm,
    ComponentsInlineFormset,
    ComponentNicknameForm,
    MoveNicknameForm
)

class ComponentDemonstrationVideoInline(admin.TabularInline):
    """Inline admin to link to a demonstation video for a component"""
    model = ComponentDemonstrationVideo
    form = VideoEntryForm
    formset = VideosFormset
    max_num = 20

class ComponentTutorialVideoInline(admin.TabularInline):
    """Inline admin to link to a tutorial video for a component"""
    model = ComponentTutorialVideo
    form = VideoEntryForm
    formset = VideosFormset
    max_num = 20


class ComponentNicknamesInline(admin.TabularInline):
    """ Inline admin for associating component nicknames with the underlying Component obejcts """
    model = ComponentNickname
    form = ComponentNicknameForm
    max_num = 20
    extra = 1

class ComponentTipsInline(admin.StackedInline):
    """ Inline admin for component tips"""
    model = ComponentTips
    max_num = 1

class ComponentAdmin(admin.ModelAdmin):
    """Admin helper for the components"""
    fields = ('name',)
    inlines = (
        ComponentTipsInline,
        ComponentDemonstrationVideoInline,
        ComponentTutorialVideoInline,
        ComponentNicknamesInline,
    )


class MoveDemonstrationVideoInline(admin.TabularInline):
    """Inline admin to link to a demonstation video for a Move"""
    model = MoveDemonstrationVideo
    form = VideoEntryForm
    formset = VideosFormset
    max_num = 20

class MoveTutorialVideoInline(admin.TabularInline):
    """Inline admin to link to a tutorial video for a Move"""
    model = MoveTutorialVideo
    form = VideoEntryForm
    formset = VideosFormset
    max_num = 20

class MoveComponentSequenceInline(admin.TabularInline):
    """ Inline admin for the move sequences. This is so we can edit the components
    sequence in the same place in the Admin page as the moves"""
    model = MoveComponentSequence
    formset = ComponentsInlineFormset
    max_num = 20 #maximum of 20 components allowed
    extra = 1

class MoveNicknamesInline(admin.TabularInline):
    """ Inline admin for associating move nicknames with the underlying move obejcts """
    model = MoveNickname
    form = MoveNicknameForm
    max_num = 20
    extra = 1

class MoveTipsInline(admin.StackedInline):
    """ Inline admin for Move tips"""
    model = MoveTips
    max_num = 1

class MoveAdmin(admin.ModelAdmin): 
    """Admin helper for the moves """
    inlines = (
        MoveComponentSequenceInline,
        MoveTipsInline,
        MoveDemonstrationVideoInline,
        MoveTutorialVideoInline,
        MoveNicknamesInline,
    )


admin.site.register(Component, ComponentAdmin)
admin.site.register(Move, MoveAdmin)
