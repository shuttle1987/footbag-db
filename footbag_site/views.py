from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.contrib.auth import authenticate, login

def error404(request):
    return render(request,'404.html')

def user_login(request):
    """Login page"""
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/user_panel/')
            else:
                return HttpResponse('Your account is currently disabled')
        else:
            return HttpResponse("invalid username or password")
    else:
        login_template = loader.get_template('login.html')
        return HttpResponse(login_template.render(context))
        #return render_to_response('/login.html', {}, context)


