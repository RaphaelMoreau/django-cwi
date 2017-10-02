from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Login URL
    url(    r'^login/$',
            auth_views.LoginView.as_view(template_name='www/login.html'),
            name='login'),
    # Logout URL
    url(    r'^logout/$',
            auth_views.LogoutView.as_view(template_name='www/logged_out.html'),
            name='logout'),
    # Application list URL
    url(    r'^$',
            views.applicationListView.as_view(),
            name='applicationList'),
    # Application detail URL
    url(    r'app/(?P<pk>[0-9]+)/$',
            views.applicationDetailView.as_view(),
            name='applicationDetail'),
    # Application update URL
    url(    r'app/(?P<pk>[0-9]+)/modify$',
            views.applicationUpdateView.as_view(),
            name='applicationUpdate'),
    # Application creation URL
    url(    r'app/create/$',
            views.applicationCreateView.as_view(),
            name='applicationCreate'),
    # new Application country URL
    url(    r'app/(?P<pk>[0-9]+)/addCountry$',
            views.applicationAddCountryView.as_view(),
            name='applicationAddCountry'),
    # Remove application country URL
    url(    r'app/(?P<appId>[0-9]+)/cty/(?P<confId>([A-Z]{2}|\*))/del$',
            views.applicationDelCountryView.as_view(),
            name='applicationDelCountry'),
    # new application platform for a country URL
    url(    r'app/(?P<appId>[0-9]+)/cty/(?P<ctyId>[0-9]+)/addPlatform$',
            views.applicationAddPlatformView.as_view(),
            name='applicationAddPlatform'),
    # Remove an application country from a platform
    url(    r'app/(?P<appId>[0-9]+)/plf/(?P<pk>[0-9]+)/del$',
            views.applicationDelPlatformView.as_view(),
            name='applicationDelPlatform'),
    # New ad type for an application platform URL
    url(    r'app/(?P<appId>[0-9]+)/plf/(?P<plfId>[0-9]+)/typ/add$',
            views.applicationAddAdTypeView.as_view(),
            name='applicationAddAdType'),
    # remove an application adtype from a platform URL
    url(    r'app/(?P<appId>[0-9]+)/typ/(?P<pk>[0-9]+)/del$',
            views.applicationDelAdTypeView.as_view(),
            name='applicationDelAdType'),
    # new ad place for a given application platform and ad type
    url(    r'app/(?P<appId>[0-9]+)/typ/(?P<typId>[0-9]+)/plc/add$',
            views.applicationAddAdPlaceView.as_view(),
            name='applicationAddAdPlace'),
    # remove an ad place from a give application platform and ad type
    url(    r'app/(?P<appId>[0-9]+)/plc/(?P<pk>[0-9]+)/del$',
            views.applicationDelAdPlaceView.as_view(),
            name='applicationDelAdPlace'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
