from django.http import HttpResponse
from django.template import loader

from django.core import serializers

from apps.footbagmoves.models import Component, Move
import json

def jsonComponents():
    """Serialize components into json"""
    all_component_objects = list(Component.objects.all())
    data = serializers.serialize('json', all_component_objects)
    return data

def jsonMoves():
    """Serialize footbag moves into json"""
    all_move_objects = list(Move.objects.all())
    json_results = [move.as_json() for move in all_move_objects]
    return json.dumps(json_results)

def index(request):
    template = loader.get_template('footbagmoves/developer.html')
    html = template.render({}, request)
    return HttpResponse(html)

def jsonComponentsView(request):
    """Respond to a request for the json serialization of the footbag components"""
    components_json = jsonComponents()
    return HttpResponse(components_json, content_type='application/json')

def jsonMovesView(request):
    """Respond to a request for the json serialization of the footbag moves"""
    moves_json = jsonMoves()
    return HttpResponse(moves_json, content_type='application/json')
