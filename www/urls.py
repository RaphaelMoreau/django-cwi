from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(    r'^login/$',
            auth_views.LoginView.as_view(template_name='www/login.html'),
            name='login'),
    url(    r'^logout/$',
            auth_views.LogoutView.as_view(template_name='www/logged_out.html'),
            name='logout'),
    url(    r'^$',
            views.applicationListView.as_view(),
            name='applicationList'),
    url(    r'app/(?P<pk>[0-9]+)/$',
            views.applicationDetailView.as_view(),
            name='applicationDetail'),
    url(    r'app/(?P<pk>[0-9]+)/modify$',
            views.applicationUpdateView.as_view(),
            name='applicationUpdate'),
    url(    r'app/create/$',
            views.applicationCreateView.as_view(),
            name='applicationCreate'),
    url(    r'app/(?P<pk>[0-9]+)/addCountry$',
            views.applicationAddCountryView.as_view(),
            name='applicationAddCountry'),
    url(    r'app/(?P<appId>[0-9]+)/cty/(?P<confId>([A-Z]{2}|\*))/del$',
            views.applicationDelCountryView.as_view(),
            name='applicationDelCountry'),
    url(    r'app/(?P<appId>[0-9]+)/cty/(?P<ctyId>[0-9]+)/addPlatform$',
            views.applicationAddPlatformView.as_view(),
            name='applicationAddPlatform'),
    url(    r'app/(?P<appId>[0-9]+)/plf/(?P<pk>[0-9]+)/del$',
            views.applicationDelPlatformView.as_view(),
            name='applicationDelPlatform'),
    url(    r'app/(?P<appId>[0-9]+)/plf/(?P<plfId>[0-9]+)/typ/add$',
            views.applicationAddAdTypeView.as_view(),
            name='applicationAddAdType'),
    url(    r'app/(?P<appId>[0-9]+)/typ/(?P<pk>[0-9]+)/del$',
            views.applicationDelAdTypeView.as_view(),
            name='applicationDelAdType'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
