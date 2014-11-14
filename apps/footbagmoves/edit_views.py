from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader

from apps.footbagmoves.models import Component
from apps.footbagmoves.forms import ComponentEditForm, SearchForm

@login_required
def component_edit(request, component_id=None):
    """Edit a component or add a new one"""
    if component_id is None:
        edit_form = ComponentEditForm()
    else:
        current_component = Component.objects.get(pk=component_id)
        data = {
            'name': current_component.name,
        }
        edit_form = ComponentEditForm()
    context = RequestContext(request, {
        'edit_form': edit_form,
    })
    template = loader.get_template('footbagmoves/component_edit.html')
    return HttpResponse(template.render(context))

