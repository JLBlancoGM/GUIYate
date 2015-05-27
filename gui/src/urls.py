from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'src.views.home', name='home'),
                       url(r'^dhcp/$', 'src.views.dhcpconf', name='dhcpconf'),
                       url(r'^sip/$', 'src.views.sipconf', name='sipconf'),)
