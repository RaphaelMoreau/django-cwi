from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Application

class applicationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Application

class applicationListView(LoginRequiredMixin, generic.ListView):
    model = Application

class applicationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Application
    fields = [ 'name', 'cryptoKey', 'icon' ]

    def get_success_url(self):
        return reverse('applicationDetail',args=(self.object.id,))

class applicationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Application
    fields = [ 'name', 'cryptoKey', 'icon' ]

    def get_success_url(self):
        return reverse('applicationDetail',args=(self.object.id,))
