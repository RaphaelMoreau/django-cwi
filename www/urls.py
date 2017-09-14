from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='www/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='www/logged_out.html'), name='logout'),
    url(r'^$', views.index, name='index'),
]
