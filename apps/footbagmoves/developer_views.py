from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('footbagmoves/developer.html')
    html = template.render({}, request)
    return HttpResponse(html)
