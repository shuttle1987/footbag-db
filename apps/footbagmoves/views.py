from django.shortcuts import render
from django.http import HttpResponse  

def move_view(request):
    return render(request, 'move_index.html')

def move_index(request):
    return HttpResponse("You're currently at the move index.")

def component_index(request):
    return HttpResponse("You're currently at the component index.")
