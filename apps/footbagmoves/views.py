""" Views for the footbag moves and components """
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader

from apps.footbagmoves.models import Component, Move, MoveComponentSequence

def move_index(request):
    """ View for the moves index page """
    template = loader.get_template('footbagmoves/move_index.html')
    latest_moves = Move.objects.all()
    num_moves = Move.objects.count()
    context = RequestContext(request,{
        'number_of_moves': num_moves,
        'recent_moves': latest_moves,
    })
    return HttpResponse(template.render(context))

def move_detail(request, move_slug):
    """ View for the move details page"""
    try:
        #extract move information object
        current_move = Move.objects.get(slug=move_slug)
    except Move.DoesNotExist:
        template = loader.get_template('footbagmoves/move_not_found.html')
        context = RequestContext(request, {'move_slug' : move_slug})
        return HttpResponseNotFound(template.render(context))
    template = loader.get_template('footbagmoves/move_detail.html')
    #load move info from DB
    components_seq = MoveComponentSequence.objects.filter(move__exact=current_move)
    demo_video = MoveDemonstrationVideo.objects.filter(component__exact=current_move)
    tutorial_video = MoveTutorialVideo.objects.filter(component__exact=current_move)
    context = RequestContext(request, {
        'move' : current_move,
        'sequence': components_seq,
        'video_demo_URL': demo_video,
        'video_tutorial_URL': tutorial_video,
    })
    return HttpResponse(template.render(context))

def component_index(request):
    """ View for the components index page """
    template = loader.get_template('footbagmoves/component_index.html')
    latest_components = Component.objects.all()
    num_components = Component.objects.count()
    context = RequestContext(request, {
        'number_of_components': num_components,
        'recent_components': latest_components,
    })
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
    #load component info from DB
    demo_video = ComponentDemonstrationVideo.objects.filter(component__exact=current_component)
    tutorial_video = ComponentTutorialVideo.objects.filter(component__exact=current_component)
    context = RequestContext(request, {
        'component' : component,
        'video_demo_URL': demo_video,
        'video_tutorial_URL': tutorial_video,
    })
    return HttpResponse(template.render(context))
