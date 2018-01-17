
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views

from social_auth_app import views as app_views

from django.views.generic import RedirectView


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', app_views.LoginView.as_view(), name='login' ),
    url(r'^home/$', app_views.home, name='home'),
    url(r'^profile/user/$', app_views.InductionView.as_view(), name='profile'),
    url(r'^logout/$', app_views.logout, name='logout'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^accounts/login/$', RedirectView.as_view(url='/'))
)
