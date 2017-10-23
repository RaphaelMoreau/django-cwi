from django import forms
from django.forms import widgets

from .models import *

class ApplicationAddCountryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.application_id = kwargs.pop('application_id')
        super(ApplicationAddCountryForm, self).__init__(*args, **kwargs)
        if self.application_id:
            q = Country.objects.filter(display=True).exclude(codeA2__in=ApplicationCountry.objects.filter(application_id=self.application_id).values_list('country')).order_by('codeA2')
            if q.count() < 6:
                self.fields['country'].widget = forms.RadioSelect()
            self.fields['country'].queryset = q
            self.fields['country'].empty_label = None
            self.fields['country'].label = ''

    class Meta:
        model = ApplicationCountry
        fields = ['country']

class ApplicationAddPlatformForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.country_id = kwargs.pop('ctyId')
        super(ApplicationAddPlatformForm, self).__init__(*args, **kwargs)
        if self.country_id:
            q = Platform.objects.exclude(id__in=ApplicationPlatform.objects.filter(country=self.country_id).values('platform'))
            if q.count() < 6:
                self.fields['platform'].widget = forms.RadioSelect()
            self.fields['platform'].queryset = q
            self.fields['platform'].empty_label = None
            self.fields['platform'].label = ''

    class Meta:
        model = ApplicationPlatform
        fields = ['platform']

class ApplicationAddAdTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.platform_id = kwargs.pop('plfId')
        super(ApplicationAddAdTypeForm, self).__init__(*args, **kwargs)
        if self.platform_id:
            q = AdType.objects.exclude(id__in=ApplicationAdType.objects.filter(platform=self.platform_id).values('adType'))
            if q.count() < 6:
                self.fields['adType'].widget = forms.RadioSelect()
            self.fields['adType'].queryset = q
            self.fields['adType'].empty_label = None
            self.fields['adType'].label = ''

    class Meta:
        model = ApplicationAdType
        fields = ['adType']

class ApplicationAddAdPlaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.adtype_id = kwargs.pop('typId')
        super(ApplicationAddAdPlaceForm, self).__init__(*args, **kwargs)
        if self.adtype_id:
            q = AdPlace.objects.exclude(id__in=ApplicationAdPlace.objects.filter(adType=self.adtype_id).values('adPlace'))
            if q.count() < 6:
                self.fields['adPlace'].widget = forms.RadioSelect()
            self.fields['adPlace'].queryset = q
            self.fields['adPlace'].empty_label = None
            self.fields['adPlace'].label = ''

    class Meta:
        model = ApplicationAdPlace
        fields = ['adPlace']

import re

class ParametersForm(forms.Form):

    def _change_field_class(self, field, add=None, remove=None):
        #fetch the widget
        widget = field.field.widget if isinstance(field, forms.BoundField) else field.widget
        #get the classes as a list
        classes = widget.attrs.get("class")
        classes = () if classes is None else str.split(classes)
        #add the class if it is not already set
        if add and add not in classes:
            classes.append(add)
        #remove the class if it is set
        if remove and remove in classes:
            classes.remove(remove)
        #update the widget classes
        widget.attrs.update({'class':' '.join(classes)})

    def param_field(self, param):
        attrs = {
            'label': param.name,
            'required': False,
        }
        #define disabled if needed
        attrs['disabled']=not param.editable
        #define initial value
        attrs['initial']=param.effective_value()
        #create the field
        if param.type == Parameter.STRING:
            field=forms.CharField(max_length=100, **attrs) #TODO use model max length !
            cls = 'param_string'
        elif param.type == Parameter.INTEGER:
            field=forms.IntegerField(**attrs)
            cls = 'param_integer'
        elif param.type == Parameter.PERCENTAGE:
            field=forms.IntegerField(min_value=0, max_value=100, **attrs)
            cls = 'param_percentage'
        elif param.type == Parameter.FLOAT:
            field=forms.FloatField(**attrs)
            cls = 'param_percentage'
        elif param.type == Parameter.BOOLEAN:
            field=forms.BooleanField(**attrs)
            cls = 'param_boolean'
        else:
            raise Exception('Unknown parameter type')
        #Set widget attributes
        field.widget.attrs.update({'default':param.default, 'class':cls})
        #hide the field if needed
        if not param.mandatory and not param.value:
            self._change_field_class(field,add='hidden_param')
        #add field
        self.fields['param_%s' % param.id] = field
        #add hidden field
        self.fields['param_%s_act' % param.id] = forms.CharField(required=False, widget=forms.HiddenInput(), initial='' if param.mandatory or param.value else 'unset')

    def parameters_fields(self):
        for param in self.parameters:
            field = self['param_%s' % param.id]
            if field.errors:
                self._change_field_class(field, remove='hidden_param')
            yield(field, param)

    def __init__(self, *args, **kwargs):
        self.parameters = kwargs.pop('parameters')
        super(ParametersForm, self).__init__(*args, **kwargs)
        if self.parameters:
            for p in self.parameters:
                self.param_field(p)

    def clean(self):
        data = super(ParametersForm, self).clean()
        rgxp = re.compile('^param_(\d+)_act$')
        cleaned = {}
        to_remove = []
        #process all fields
        for k,v in data.items():
            res = rgxp.match(k)
            if res:
                id=int(res.group(1))
                name = 'param_%s' %id
                if v == 'del':
                    #remove (potential) error for this field
                    self.errors.pop(name, None)
                    #store name to remove value from cleaned data
                    to_remove.append(name)
                elif v == 'add':
                    #remove (potential) class hidden for param. If there is an error, field may not be displayed. Force display
                    self._change_field_class(self.fields[name],remove='hidden_param')
                elif v == 'unset':
                    #field should not be defined if optional and still unset
                    to_remove.append(name)
            else:
                #now add field to cleaned data
                cleaned[k] = v
        #now remove "deleted" fields
        for k in to_remove:
            cleaned.pop(k, None)
        return cleaned
