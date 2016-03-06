from django.http import HttpResponse
from django.template import loader

from django.core import serializers

from apps.footbagmoves.models import Component

def jsonComponents():
    """Serialize components into json"""
    all_component_objects = list(Component.objects.all())
    data = serializers.serialize('json', all_component_objects)
    return data

def index(request):
    template = loader.get_template('footbagmoves/developer.html')
    html = template.render({}, request)
    return HttpResponse(html)

def jsonComponentsView(request):
    """Respond to a request for the json serialization of the footbag components"""
    components_json = jsonComponents()
    return HttpResponse(components_json, content_type='application/json')
