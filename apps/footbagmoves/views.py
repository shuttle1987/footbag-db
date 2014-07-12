""" Views for the footbag moves and components """
from django.shortcuts import render
from django.http import HttpResponse  
from django.template import RequestContext, loader

def move_view(request):
    return render(request, 'move_index.html')

def move_index(request):
    return HttpResponse("You're currently at the move index.")

def component_index(request):
    template = loader.get_template('footbagmoves/component_index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
