from django import forms

from .models import *

class ApplicationAddCountryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.application_id = kwargs.pop('application_id')
        super(ApplicationAddCountryForm, self).__init__(*args, **kwargs)
        if self.application_id:
            self.fields['country'].queryset = Country.objects.filter(display=True).exclude(codeA2__in=ApplicationCountry.objects.filter(application_id=self.application_id).values_list('country')).order_by('codeA2')

    class Meta:
        model = ApplicationCountry
        fields = ['country']

class ApplicationAddPlatformForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.country_id = kwargs.pop('ctyId')
        super(ApplicationAddPlatformForm, self).__init__(*args, **kwargs)
        if self.country_id:
            self.fields['platform'].queryset = Platform.objects.exclude(id__in=ApplicationPlatform.objects.filter(country=self.country_id).values_list('platform'))

    class Meta:
        model = ApplicationPlatform
        fields = ['platform']

class ApplicationAddAdPlaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.adtype_id = kwargs.pop('typId')
        super(ApplicationAddAdPlaceForm, self).__init__(*args, **kwargs)
        if self.adtype_id:
            self.fields['adPlace'].queryset = AdPlace.objects.exclude(id__in=ApplicationAdPlace.objects.filter(adType=self.adtype_id).values_list('adPlace_id'))

    class Meta:
        model = ApplicationAdPlace
        fields = ['adPlace']
