from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.forms.models import inlineformset_factory
from django.template.defaultfilters import slugify

from apps.footbagmoves.models import Component, ComponentDemonstrationVideo
from apps.footbagmoves.forms import ComponentEditForm, VideoEntryForm, VideosFormset

VideoEntryFormset = inlineformset_factory(Component, ComponentDemonstrationVideo, form=VideoEntryForm, formset=VideosFormset, extra=1, max_num=20)

@login_required
def component_edit(request, component_id=None):
    """Edit a component or add a new one"""
    if component_id is None:
        new_component = Component()
        edit_form = ComponentEditForm(request.POST or None)
        demo_vids = VideoEntryFormset(request.POST or None, instance=new_component)
        if demo_vids.is_valid() and edit_form.is_valid():
            new_component.name = edit_form.cleaned_data.get("name")
            existing_components = Component.objects.filter(slug=slugify(new_component.name))
            if not existing_components:
                new_component.save()
                demo_vids.save()
                return HttpResponseRedirect(reverse('component_detail', args=[new_component.slug]))
            else:
                return HttpResponse("component with slug {0} already exists!".format(slugify(new_component.name)))
    else:
        current_component = get_object_or_404(Component, pk=component_id)
        demo_vids = VideoEntryFormset(request.POST or None, instance=current_component)
        if current_component and demo_vids.is_valid():
            print("Valid component and Valid formset!!")
        data = {
            'name': current_component.name,
        }
        edit_form = ComponentEditForm(data)

    context = RequestContext(request, {
        'edit_form': edit_form,
        'demo_vids': demo_vids,
    })
    template = loader.get_template('footbagmoves/component_edit.html')
    return HttpResponse(template.render(context))

