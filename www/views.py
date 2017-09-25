from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *

# List of applications
class applicationListView(LoginRequiredMixin, generic.ListView):
    model = Application

# detailed view of an application
class applicationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super(applicationDetailView, self).get_context_data(**kwargs)
        context['countries_count'] = Country.objects.filter(display=True).count
        context['platforms_count'] = Platform.objects.count
        context['ads_count'] = AdType.objects.count() * AdPlace.objects.count()
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
from .forms import *

class applicationAddAdConfigurationView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationAdConfig
    form_class = ApplicationAddAdConfigForm

    def get_form_kwargs(self):
        kwargs = super(applicationAddAdConfigurationView, self).get_form_kwargs()
        kwargs['application_id'] = self.kwargs['pk']
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
            form.add_error(None, e)
            return self.form_invalid(form)
        response = super(applicationAddAdConfigurationView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationAddAdConfigurationView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['pk'])
        return context

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

    def get_context_data(self, **kwargs):
        context = super(applicationDelAdConfigurationView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        return context

# Adding a platform to an application config (country)
class applicationAddPlatformView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationPlatform
    form_class = ApplicationAddPlatformForm

    def get_form_kwargs(self):
        kwargs = super(applicationAddPlatformView, self).get_form_kwargs()
        kwargs['cfgId']=self.kwargs['cfgId']
        return kwargs

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        config = get_object_or_404(ApplicationAdConfig, pk=self.kwargs['cfgId'])
        form.instance.config = config
        from django.core.exceptions import ValidationError
        try:
            form.instance.validate_unique()
        except ValidationError as e:
            form.add_error(None,e)
            return self.form_invalid(form)
        response = super(applicationAddPlatformView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationAddPlatformView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        context['config'] = get_object_or_404(ApplicationAdConfig, pk=self.kwargs['cfgId'])
        return context

# Remove a platform from an application config (country)
class applicationDelPlatformView(LoginRequiredMixin, generic.DeleteView):
    model = ApplicationPlatform

    def get_success_url(self):
        return '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationDelPlatformView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        context['platform'] = get_object_or_404(ApplicationPlatform, pk=self.kwargs['pk'])
        return context

# Adding an ad to a platform (which is linked to a config, which is linked to an application)
class applicationAddAdView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationAd
    fields = [ 'adType', 'adPlace' ]

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        platform = get_object_or_404(ApplicationPlatform, pk=self.kwargs['plfId'])
        form.instance.platform = platform
        from django.core.exceptions import ValidationError
        try:
            form.instance.validate_unique()
        except ValidationError as e:
            form.add_error(None,e)
            return self.form_invalid(form)
        response = super(applicationAddAdView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationAddAdView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        context['platform'] = get_object_or_404(ApplicationPlatform, pk=self.kwargs['plfId'])
        return context

# Remove an ad from a platform
class applicationDelAdView(LoginRequiredMixin, generic.DeleteView):
    model = ApplicationAd

    def get_success_url(self):
        return '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationDelAdView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        #context['platform'] = get_object_or_404(ApplicationPlatform, pk=self.kwargs['pk'])
        return context
