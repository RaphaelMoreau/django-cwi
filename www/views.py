from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Application

@login_required()
def index(request):
    apps = Application.objects.all()
    context = {
        'apps': apps
    }
    return render(request, 'www/index.html', context)

def appDetail(request, pk):
    return HttpResponse("Display application "+pk)

def appCreate(request):
    return HttpResponse("Creating a new application")
