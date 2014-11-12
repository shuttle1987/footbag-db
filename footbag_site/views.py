from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def error404(request):
    return render(request, '404.html', status=404)

def error500(request):
    return render(request, '500.html', status=500)

@login_required
def user_panel(request):
    """User account panel"""
    context = RequestContext(request)
    login_template = loader.get_template('user_panel.html')
    return HttpResponse(login_template.render(context))
