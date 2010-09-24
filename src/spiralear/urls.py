from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from spiralear.website import urls

urlpatterns = patterns('',
    # Example:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT,
                               'show_indexes': True}),
    (r'^pl/', include(urls.pl)),
    (r'^en/', include(urls.en)),
    (r'^', 'spiralear.website.views.redirect'),
)
