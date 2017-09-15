from django.contrib import admin

from .models import Application, Country, ApplicationAdConfig, Platform, AdType, AdPlace

# Register your models here.
admin.site.register(Application)
admin.site.register(Country)
admin.site.register(ApplicationAdConfig)
admin.site.register(Platform)
admin.site.register(AdType)
admin.site.register(AdPlace)
