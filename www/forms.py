from django import forms

from .models import ApplicationAdConfig, Country

class ApplicationAddAdConfigForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.application_id = kwargs.pop('application_id')
        super(ApplicationAddAdConfigForm, self).__init__(*args, **kwargs)
        if self.application_id:
            self.fields['country'].queryset = Country.objects.filter(display=True).exclude(codeA2__in=ApplicationAdConfig.objects.filter(application_id=self.application_id).values_list('country')).order_by('codeA2')

    class Meta:
        model = ApplicationAdConfig
        fields = ['country']
