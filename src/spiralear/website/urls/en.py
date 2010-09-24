from django.conf.urls.defaults import *

from spiralear.website.models import Language

en_id = Language.en.id
lang_en = {'lang': en_id}

urlpatterns = patterns('spiralear.website.views',
        url(r'^$', 'handler', kwargs={'page': 'frontpage', 'lang': en_id}),
        url(r'^(?P<page>products)/$', 'handler', kwargs=lang_en),
        url(r'^(?P<page>gallery)/$', 'handler', kwargs=lang_en),
        url(r'^(?P<page>ordering)/$', 'handler', kwargs=lang_en),
        url(r'^(?P<page>contact)/$', 'handler', kwargs=lang_en))
