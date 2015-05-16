from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'src.views.home', name='home'),
)
