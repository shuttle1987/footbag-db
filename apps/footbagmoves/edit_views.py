from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.forms.models import inlineformset_factory
from django.template.defaultfilters import slugify

from apps.footbagmoves.models import Component, ComponentDemonstrationVideo, ComponentTutorialVideo, ComponentTips
from apps.footbagmoves.models import Move, MoveComponentSequence, MoveDemonstrationVideo, MoveTutorialVideo, MoveTips
from apps.footbagmoves.forms import ComponentEditForm, ComponentsInlineFormset,  MoveEditForm, VideoEntryForm, VideosFormset, TipsForm, MoveComponentSequenceForm

#Formset for component demonstration videos
ComponentDemoVideoFormset = inlineformset_factory(
    Component,
    ComponentDemonstrationVideo,
    form=VideoEntryForm,
    formset=VideosFormset,
    extra=1,
    max_num=20,
    can_delete=True,
)

#Formset for component tutorial videos
ComponentTutorialVideoFormset = inlineformset_factory(
    Component,
    ComponentTutorialVideo,
    form=VideoEntryForm,
    formset=VideosFormset,
    extra=1,
    max_num=20,
    can_delete=True,
)

#Formset for move demonstration videos
MoveDemoVideoFormset = inlineformset_factory(
    Move,
    MoveDemonstrationVideo,
    form=VideoEntryForm,
    formset=VideosFormset,
    extra=1,
    max_num=20
)

#Formset for move tutorial videos
MoveTutorialVideoFormset = inlineformset_factory(
    Move,
    MoveTutorialVideo,
    form=VideoEntryForm,
    formset=VideosFormset,
    extra=1,
    max_num=20

)

#Formset for entering in the sequence of components in a move
ComponentSequenceFormset = inlineformset_factory(
    Move,
    MoveComponentSequence,
    form=MoveComponentSequenceForm,
    formset=ComponentsInlineFormset,
    extra=1,
    max_num=15
)

@login_required
def component_new(request):
    """Add a new component to the database"""
    new_component = Component()
    edit_form = ComponentEditForm(request.POST or None)
    tips_form = TipsForm(request.POST or None)
    demo_vids = ComponentDemoVideoFormset(request.POST or None, instance=new_component)
    if demo_vids.is_valid() and edit_form.is_valid():
        new_component.name = edit_form.cleaned_data.get("name")
        existing_components = Component.objects.filter(slug=slugify(new_component.name))
        if existing_components:
            return HttpResponse("Error saving: component with slug {0} already exists!".format(slugify(new_component.name)))
        else:
            new_component.save()
            demo_vids.save()
            if tips_form.is_valid():
                ComponentTips.objects.create(
                    component=new_component,
                    tips=tips_form.cleaned_data.get("tips"),
                    tips_markup_type='markdown',
                )
            return HttpResponseRedirect(reverse('component_detail', args=[new_component.slug]))

    context = RequestContext(request, {
        'add_new': True, #Flag for template
        'edit_form': edit_form,
        'tips_form': tips_form,
        'demo_vids': demo_vids,
    })
    template = loader.get_template('footbagmoves/component_modify.html')
    return HttpResponse(template.render(context))

@login_required
def component_modify(request, component_id):
    """Modify an existing component in the database:
    :component_id: the unique id of the component being modified"""
    current_component = get_object_or_404(Component, pk=component_id)
    demo_vids = ComponentDemoVideoFormset(request.POST or None, instance=current_component)
    try: #load tips if possible
        existing_tips = ComponentTips.objects.get(component=current_component)
        tips_form = TipsForm(request.POST or {'tips': existing_tips.tips.raw})
    except ComponentTips.DoesNotExist:
        existing_tips = None
        tips_form = TipsForm(request.POST or None)

    data = {
        'name': current_component.name,
    }
    edit_form = ComponentEditForm(data)
    if demo_vids.is_valid() and edit_form.is_valid() and tips_form.is_valid():
        demo_vids.save()
        if existing_tips:
            existing_tips.tips.raw = tips_form.cleaned_data.get("tips")
            existing_tips.save()
        else:
            ComponentTips.objects.create(
                component=current_component,
                tips=tips_form.cleaned_data.get("tips"),
                tips_markup_type='markdown',
            )
        return HttpResponseRedirect(reverse('component_detail', args=[current_component.slug]))

    context = RequestContext(request, {
        'component_name': current_component.name,
        'edit_form': edit_form,
        'tips_form': tips_form,
        'demo_vids': demo_vids,
        'add_new': False,
    })
    template = loader.get_template('footbagmoves/component_modify.html')
    return HttpResponse(template.render(context))


@login_required
def move_new(request):
    """Add a new move to the database"""
    new_move = Move()
    edit_form = MoveEditForm(request.POST or None)
    component_sequence = ComponentSequenceFormset(request.POST or None, instance=new_move)
    tips_form = TipsForm(request.POST or None)
    demo_vids = MoveDemoVideoFormset(request.POST or None, instance=new_move)
    if demo_vids.is_valid() and edit_form.is_valid():
        new_move.name = edit_form.cleaned_data.get("name")
        existing_moves = Move.objects.filter(slug=slugify(new_move.name))
        if existing_moves:
            return HttpResponse("Error saving: move with slug {0} already exists!".format(slugify(new_move.name)))
        else:
            new_move.save()
            demo_vids.save()
            if tips_form.is_valid():
                MoveTips.objects.create(
                    move=new_move,
                    tips=tips_form.cleaned_data.get("tips"),
                    tips_markup_type='markdown',
                )
            return HttpResponseRedirect(reverse('move_detail', args=[new_move.slug]))

    context = RequestContext(request, {
        'edit_form': edit_form,
        'component_sequence': component_sequence,
        'tips_form': tips_form,
        'demo_vids': demo_vids,
    })
    template = loader.get_template('footbagmoves/move_new.html')
    return HttpResponse(template.render(context))

@login_required
def move_modify(request, move_id):
    """Modify an existing move in the database:
    :move_id: the unique id of the move being modified"""
    current_move = get_object_or_404(Move, pk=move_id)
    demo_vids = MoveDemoVideoFormset(request.POST or None, instance=current_move)
    try: #load tips if possible
        existing_tips = MoveTips.objects.get(move=current_move)
        tips_form = TipsForm(request.POST or {'tips': existing_tips.tips.raw})
    except MoveTips.DoesNotExist:
        existing_tips = None
        tips_form = TipsForm(request.POST or None)

    data = {
        'name': current_move.name,
    }
    edit_form = MoveEditForm(data)
    component_sequence = ComponentSequenceFormset(request.POST or None, instance=current_move)
    if demo_vids.is_valid() and edit_form.is_valid() and tips_form.is_valid():
        demo_vids.save()
        if existing_tips:
            existing_tips.tips.raw = tips_form.cleaned_data.get("tips")
            existing_tips.save()
        else:
            MoveTips.objects.create(
                move=current_move,
                tips=tips_form.cleaned_data.get("tips"),
                tips_markup_type='markdown',
            )
        return HttpResponseRedirect(reverse('move_detail', args=[current_move.slug]))

    context = RequestContext(request, {
        'move_name': current_move.name,
        'edit_form': edit_form,
        'component_sequence': component_sequence,
        'tips_form': tips_form,
        'demo_vids': demo_vids,
    })
    template = loader.get_template('footbagmoves/move_modify.html')
    return HttpResponse(template.render(context))

