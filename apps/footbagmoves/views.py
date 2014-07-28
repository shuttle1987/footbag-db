""" Views for the footbag moves and components """
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader

from apps.footbagmoves.models import Component, Move

def move_index(request):
    """ View for the moves index page """
    template = loader.get_template('footbagmoves/move_index.html')
    latest_moves = Move.objects.all()
    context = RequestContext(request, {'recent_moves': latest_moves})
    return HttpResponse(template.render(context))

def move_detail(request):
    """ View for the move details page"""
    pass

def component_index(request):
    """ View for the components index page """
    template = loader.get_template('footbagmoves/component_index.html')
    latest_components = Component.objects.all()
    context = RequestContext(request, {'recent_components': latest_components})
    return HttpResponse(template.render(context))

def component_detail(request, component_slug):
    """ View for the details of an individual component.
    If the component is found in the database the component_detail template is loaded
    and if not the component_not_found template is loaded."""
    try:
        component = Component.objects.get(slug=component_slug)
    except Component.DoesNotExist:
        template = loader.get_template('footbagmoves/component_not_found.html')
        context = RequestContext(request, {'component_slug' : component_slug})
        return HttpResponseNotFound(template.render(context))
    template = loader.get_template('footbagmoves/component_detail.html')
    context = RequestContext(request, {'component' : component})
    return HttpResponse(template.render(context))
