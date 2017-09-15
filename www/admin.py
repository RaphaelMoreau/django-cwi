from django.contrib import admin

from .models import Application, Country

# Register your models here.
admin.site.register(Application)
admin.site.register(Country)
