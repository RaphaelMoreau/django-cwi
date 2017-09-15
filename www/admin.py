from django.contrib import admin

from .models import Application, Country, ApplicationAdConfig

# Register your models here.
admin.site.register(Application)
admin.site.register(Country)
admin.site.register(ApplicationAdConfig)
