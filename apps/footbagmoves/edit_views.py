from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader

from django.forms.formsets import formset_factory

from apps.footbagmoves.models import Component
from apps.footbagmoves.forms import ComponentEditForm, VideoEntryForm, VideosFormset

@login_required
def component_edit(request, component_id=None):
    """Edit a component or add a new one"""
    VideoEntryFormset = formset_factory(Component, VideoEntryForm)
    if component_id is None:
        new_component = Component()
        edit_form = ComponentEditForm()
        demo_vids = VideoEntryFormset(instance=new_component)
    else:
        current_component = Component.objects.get(pk=component_id)
        demo_vids = VideoEntryFormset(instance=current_component)
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

