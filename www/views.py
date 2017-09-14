from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Application

@login_required()

def applicationList(request):
    apps = Application.objects.all()
    context = {
        'applications': apps
    }
    return render(request, 'www/application_list.html', context)

def applicationDetail(request, pk):
    app = get_object_or_404(Application, pk=pk)
    context = {
        'application': app
    }
    return render(request, "www/application_detail.html", context)

def applicationCreate(request):
    try:
        app = Application(name=request.POST['name'], cryptoKey=request.POST['key'])
    except (KeyError):
        return render(request, "www/application_create.html")
    else:
        app.save()
        return HttpResponseRedirect(reverse('applicationDetail', args=(app.id,)))
