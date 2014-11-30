from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.forms.models import inlineformset_factory
from django.template.defaultfilters import slugify

from apps.footbagmoves.models import Component, ComponentDemonstrationVideo, ComponentTips
from apps.footbagmoves.forms import ComponentEditForm, VideoEntryForm, VideosFormset, TipsForm

VideoEntryFormset = inlineformset_factory(Component, ComponentDemonstrationVideo, form=VideoEntryForm, formset=VideosFormset, extra=1, max_num=20)

@login_required
def component_modify(request, component_id):
    """Modify an existing component in the database:
    :component_id: the unique id of the component being modified"""
    current_component = get_object_or_404(Component, pk=component_id)
    demo_vids = VideoEntryFormset(request.POST or None, instance=current_component)
    try: #load tips if possible
        existing_tips = ComponentTips.objects.get(component=current_component)
        tips_form = TipsForm(request.POST or {'tips': existing_tips.tips.raw})
    except ComponentTips.DoesNotExist:
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
    })
    template = loader.get_template('footbagmoves/component_modify.html')
    return HttpResponse(template.render(context))


@login_required
def component_new(request):
    """Add a new component to the database"""
    new_component = Component()
    edit_form = ComponentEditForm(request.POST or None)
    tips_form = TipsForm(request.POST or None)
    demo_vids = VideoEntryFormset(request.POST or None, instance=new_component)
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
        'edit_form': edit_form,
        'tips_form': tips_form,
        'demo_vids': demo_vids,
    })
    template = loader.get_template('footbagmoves/component_new.html')
    return HttpResponse(template.render(context))

