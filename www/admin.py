from django.contrib import admin

from .models import *

#Defining admin site titles
admin.site.site_header = "CWI Administration"
admin.site.site_title = "CWI Administration site"
admin.site.index_title = "CWI Administration"

# Registering models
admin.site.register(Application)
admin.site.register(ApplicationAdConfig)
admin.site.register(ApplicationPlatform)
admin.site.register(ApplicationAd)
admin.site.register(Country)
admin.site.register(Platform)
admin.site.register(AdType)
admin.site.register(AdPlace)
