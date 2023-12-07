from django.shortcuts import render
from django.http import HttpResponse

def sobre(request):
    return HttpResponse('Sobre')

def contato(request):
    return HttpResponse('Contato')

def home(request):
    return render(request, 'home.html')
