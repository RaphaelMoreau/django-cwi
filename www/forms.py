from django import forms

from .models import *

class ApplicationAddAdConfigForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.application_id = kwargs.pop('application_id')
        super(ApplicationAddAdConfigForm, self).__init__(*args, **kwargs)
        if self.application_id:
            self.fields['country'].queryset = Country.objects.filter(display=True).exclude(codeA2__in=ApplicationAdConfig.objects.filter(application_id=self.application_id).values_list('country')).order_by('codeA2')

    class Meta:
        model = ApplicationAdConfig
        fields = ['country']

class ApplicationAddPlatformForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.config_id = kwargs.pop('cfgId')
        super(ApplicationAddPlatformForm, self).__init__(*args, **kwargs)
        if self.config_id:
            self.fields['platform'].queryset = Platform.objects.exclude(id__in=ApplicationPlatform.objects.filter(config=self.config_id).values_list('platform'))

    class Meta:
        model = ApplicationPlatform
        fields = ['platform']
