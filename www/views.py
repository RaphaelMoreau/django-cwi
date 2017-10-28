from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages

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
        context['adtypes_count'] = AdType.objects.count()
        context['adplaces_count'] = AdPlace.objects.count()
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

# Adding a country to an application
from .forms import *

class applicationAddCountryView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationCountry
    form_class = ApplicationAddCountryForm

    def get_form_kwargs(self):
        kwargs = super(applicationAddCountryView, self).get_form_kwargs()
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
        response = super(applicationAddCountryView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationAddCountryView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['pk'])
        return context

# Removing a country from an application
class applicationDelCountryView(LoginRequiredMixin, generic.DeleteView):
    model = ApplicationCountry

    def get_success_url(self):
        return '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_object(self):
        return get_object_or_404(ApplicationCountry, application=self.kwargs['appId'], country=self.kwargs['confId'])

    def get_context_data(self, **kwargs):
        context = super(applicationDelCountryView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        return context

# Adding a platform to an application country
class applicationAddPlatformView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationPlatform
    form_class = ApplicationAddPlatformForm

    def get_form_kwargs(self):
        kwargs = super(applicationAddPlatformView, self).get_form_kwargs()
        kwargs['ctyId']=self.kwargs['ctyId']
        return kwargs

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        country = get_object_or_404(ApplicationCountry, pk=self.kwargs['ctyId'])
        form.instance.country = country
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
        context['country'] = get_object_or_404(ApplicationCountry, pk=self.kwargs['ctyId'])
        return context

# Remove a platform from an application country
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

# Adding an ad type to an application platform (which is linked to an application country)
class applicationAddAdTypeView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationAdType
    form_class = ApplicationAddAdTypeForm

    def get_success_url(self):
        return '/'

    def get_form_kwargs(self):
        kwargs = super(applicationAddAdTypeView, self).get_form_kwargs()
        kwargs['plfId']=self.kwargs['plfId']
        return kwargs

    def form_valid(self, form):
        platform = get_object_or_404(ApplicationPlatform, pk=self.kwargs['plfId'])
        form.instance.platform = platform
        from django.core.exceptions import ValidationError
        try:
            form.instance.validate_unique()
        except ValidationError as e:
            form.add_error(None,e)
            return self.form_invalid(form)
        response = super(applicationAddAdTypeView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationAddAdTypeView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        context['platform'] = get_object_or_404(ApplicationPlatform, pk=self.kwargs['plfId'])
        return context

# Remove an ad from a platform
class applicationDelAdTypeView(LoginRequiredMixin, generic.DeleteView):
    model = ApplicationAdType

    def get_success_url(self):
        return '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationDelAdTypeView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        #context['platform'] = get_object_or_404(ApplicationPlatform, pk=self.kwargs['pk'])
        return context

# Adding an ad place to an application ad type
class applicationAddAdPlaceView(LoginRequiredMixin, generic.CreateView):
    model = ApplicationAdPlace
    form_class = ApplicationAddAdPlaceForm

    def get_form_kwargs(self):
        kwargs = super(applicationAddAdPlaceView, self).get_form_kwargs()
        kwargs['typId']=self.kwargs['typId']
        return kwargs

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        adtype = get_object_or_404(ApplicationAdType, pk=self.kwargs['typId'])
        form.instance.adType = adtype
        form.instance.platform = adtype.platform
        from django.core.exceptions import ValidationError
        try:
            form.instance.validate_unique()
        except ValidationError as e:
            form.add_error(None,e)
            return self.form_invalid(form)
        response = super(applicationAddAdPlaceView, self).form_valid(form)
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationAddAdPlaceView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        context['adtype'] = get_object_or_404(ApplicationAdType, pk=self.kwargs['typId'])
        return context

# Remove an ad place from an application ad type
class applicationDelAdPlaceView(LoginRequiredMixin, generic.DeleteView):
    model = ApplicationAdPlace

    def get_success_url(self):
        return '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("<script type='text/javascript'>window.close(); window.opener.location.reload();</script>")

    def get_context_data(self, **kwargs):
        context = super(applicationDelAdPlaceView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        return context

#Base class for parameters modification views
class baseParametersView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'www/parameters_form.html'
    form_class = ParametersForm

    def get_success_url(self):
        return self.request.get_full_path()

    def get_form_kwargs(self):
        kwargs = super(baseParametersView, self).get_form_kwargs()
        kwargs['parameters'] = get_object_or_404(self.main_class, pk=self.kwargs[self.kw_id]).parameters()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(baseParametersView, self).get_context_data(**kwargs)
        context['application'] = get_object_or_404(Application, pk=self.kwargs['appId'])
        context['object_description'] = self.main_desc
        obj = get_object_or_404(self.main_class, pk=self.kwargs[self.kw_id])
        context['object'] = obj
        context['params'] = self.param_class.get_for(obj, obj.id)
        return context

    def form_valid(self, form):
        obj = get_object_or_404(self.main_class, pk=self.kwargs[self.kw_id])
        success = False
        for p in form.parameters:
            success |= p.store(form.cleaned_data.get('param_%s' % p.id,None), obj)
        if success is True:
            messages.success(self.request, "Changes saved succesfully")
        else:
            messages.info(self.request,"No modifications")
        return super(baseParametersView, self).form_valid(form)

# View and modify an application ad type parameters
class applicationAdTypeParametersView(baseParametersView):
    main_desc = 'Ad type'
    main_class = ApplicationAdType
    param_class = AdTypeParameter
    kw_id = 'typId'

# View and modify an application ad place parameters
class applicationAdPlaceParametersView(baseParametersView):
    main_desc = 'Ad place'
    main_class = ApplicationAdPlace
    param_class = AdPlaceParameter
    kw_id = 'plcId'
