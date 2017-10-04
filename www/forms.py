from django import forms

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
