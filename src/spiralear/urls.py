from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT,
                               'show_indexes': True}),
    (r'^(?P<lang>[^/]+)/$', 'spiralear.website.views.handler',
                            {'url': ''}),
    (r'^(?P<lang>[^/]+)/(?P<url>.*)/$', 'spiralear.website.views.handler'),
    (r'^', 'spiralear.website.views.redirect'),
)
