from django.conf.urls.defaults import *

from spiralear.website.models import Language

pl_id = Language.pl.id
lang_pl = {'lang': pl_id}

urlpatterns = patterns('spiralear.website.views',
        url(r'^$', 'handler', kwargs={'page': 'glowna', 'lang': pl_id}),
        url(r'^(?P<page>produkty)/$', 'handler', kwargs=lang_pl),
        url(r'^(?P<page>galeria)/$', 'handler', kwargs=lang_pl),
        url(r'^(?P<page>zamowienia)/$', 'handler', kwargs=lang_pl),
        url(r'^(?P<page>kontakt)/$', 'handler', kwargs=lang_pl))
