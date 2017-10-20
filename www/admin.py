from django.contrib import admin

from .models import *

#Defining admin site titles
admin.site.site_header = "CWI Administration"
admin.site.site_title = "CWI Administration site"
admin.site.index_title = "CWI Administration"

# registering reference tables for admin
admin.site.register(Country)
admin.site.register(Platform)
admin.site.register(AdType)
admin.site.register(AdTypeParameter)
admin.site.register(AdPlace)

# Registering models
admin.site.register(Application)
admin.site.register(ApplicationCountry)
admin.site.register(ApplicationPlatform)
admin.site.register(ApplicationAdType)
admin.site.register(ApplicationAdTypeParameter)
admin.site.register(ApplicationAdPlace)
