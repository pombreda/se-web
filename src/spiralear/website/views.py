#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Łukasz Langa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
from datetime import datetime
from random import randint
from textwrap import dedent

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import Template, RequestContext
from django.utils.safestring import mark_safe

from langacore.kit.django.helpers import render

from spiralear.website.models import Page, Url, Content, Block, Newsfeed
from spiralear.website.models import Language


def handler(request, url, lang):
    url = url.lower()
    lang_symbol = lang.lower()
    lang = Language.IDFromName(lang_symbol, fallback=Language.en.id)
    try:
        u = Url.objects.get(url=url, lang=lang)
        c = Content.objects.get(url=u)
    except (Url.DoesNotExist, Content.DoesNotExist):
        redirect(request)

    menu = _generate_menu(lang)
    _mark_active(menu, u)
    other = [(other.full_link(), other.lang_description(long=True))
                for other in u.page.get_others()]

    c.block = BlockRenderer(request, {'domain': settings.DOMAIN})
    for b in Block.objects.filter(content=c):
        c.block.add(b)

    feed_url = "http://spiralear.com/"
    feed_content = ""
    try:
        f = Newsfeed.objects.filter(date_from__lte=datetime.now(),
                                    date_to__gte=datetime.now(),
                                    lang=lang)
        if len(f) > 0:
            f = f[0]
            feed_url = f.url
            feed_content = f.content
    except Newsfeed.DoesNotExist:
        pass
    return render(request, c.template, locals())


def redirect(request):
    return HttpResponseRedirect('/en/')


def sitemap(request):
    urls = ['http://{}/{}/{}'.format(settings.DOMAIN,
                Language.NameFromID(url.lang, fallback=''),
                ("{}/".format(url.url)) if url.url else '')
            for url in Url.objects.all()]
    return render(request, "sitemap.xml", locals(),
                  mimetype='application/xml')


def robots(request):
    return render(request, "robots.txt", locals(),
                  mimetype='text/plain')


def _generate_menu(lang, parent=None):
    menu = []
    for page in Page.objects.filter(parent=parent).order_by("index"):
        try:
            url = Url.objects.get(page=page, lang=lang)
            content = Content.objects.get(url=url)

            # ugly hack
            if url.url:
                title = content.title
            else:
                title = "SPIRAL EAR"

            children = _generate_menu(lang, page)
            menu.append({
                'title': title,
                'url': url.full_link(),
                'active': False, # will be marked after the fact
                'children': children
            })
        except (Url.DoesNotExist, Content.DoesNotExist):
            continue
    return menu


def _mark_active(menu, url):
    full_link = url.full_link()
    is_active = True
    for entry in menu:
        if entry['url'] == full_link:
            entry['active'] = True
            break
        else:
            entry['active'] = _mark_active(entry['children'], url)
    else:
        is_active = False
    return is_active


class BlockRenderer(object):
    def __init__(self, request, context=None):
        self.request = request
        self.context = context if context else {}
        self.blocks = {}

    def add(self, block):
        text = dedent("""
        {%load validation%}
        {%load descriptions%}
        """).lstrip() + block.text
        self.blocks[block.name] = Template(text)

    def __getitem__(self, key):
        r = self.request
        get = defaultdict(lambda: '')
        # cannot use dict.update() because request.GET is really
        # a multi-dict
        for k in r.GET:
            get[k] = r.GET[k]
        self.context['get'] = get
        return mark_safe(self.blocks[key].render(RequestContext(r,
                                                 self.context)))
