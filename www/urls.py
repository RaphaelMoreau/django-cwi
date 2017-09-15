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
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
