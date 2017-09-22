from django.contrib import admin

from .models import Application, Country, ApplicationAdConfig, Platform, AdType, AdPlace

#Defining admin site titles
admin.site.site_header = "CWI Administration"
admin.site.site_title = "CWI Administration site"
admin.site.index_title = "CWI Administration"

# Registering models
admin.site.register(Application)
admin.site.register(Country)
admin.site.register(ApplicationAdConfig)
admin.site.register(Platform)
admin.site.register(AdType)
admin.site.register(AdPlace)
