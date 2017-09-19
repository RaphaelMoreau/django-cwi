from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Application, Country, ApplicationAdConfig

# List of applications
class applicationListView(LoginRequiredMixin, generic.ListView):
    model = Application

# detailed view of an application
class applicationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super(applicationDetailView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.filter(display=True).count
        return context

# Creation of a new application
class applicationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Application
    fields = [ 'name', 'cryptoKey', 'icon' ]

    def get_success_url(self):
        return reverse('applicationDetail',args=(self.object.id,))

# Modification of an existing application
class applicationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Application
    fields = [ 'name', 'cryptoKey', 'icon' ]

    def get_success_url(self):
        return reverse('applicationDetail',args=(self.object.id,))

# Adding an ad configuration (country) to an application
from .forms import ApplicationAddAdConfigForm

class applicationAddAdConfigurationView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationAdConfig
    form_class = ApplicationAddAdConfigForm

    def get_form_kwargs(self):
        kwargs = super(applicationAddAdConfigurationView,self).get_form_kwargs()
        kwargs['application_id']=self.kwargs['pk']
        return kwargs

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        app = get_object_or_404(Application, pk=self.kwargs['pk'])
        form.instance.application = app
        from django.core.exceptions import ValidationError
        try:
            form.instance.validate_unique()
        except ValidationError as e:
            form.add_error(None,e)
            return self.form_invalid(form)
        response = super(applicationAddAdConfigurationView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

# Removing an ad configuration (country) to an application
class applicationDelAdConfigurationView(LoginRequiredMixin, generic.DeleteView):
    model = ApplicationAdConfig

    def get_success_url(self):
        return '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_object(self):
        return get_object_or_404(ApplicationAdConfig, application=self.kwargs['appId'], country=self.kwargs['confId'])
