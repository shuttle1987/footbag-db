""" Views for the homepage found when you go to the root URL for the site
"""
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext

def index(request):
    """ Render the requests for the homepage found at root URL """
    return render_to_response('home/index.html', context_instance=RequestContext(request))
