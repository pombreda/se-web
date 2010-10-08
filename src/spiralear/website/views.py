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
from random import randint

from django.http import HttpResponseRedirect
from django.template import Template, RequestContext
from django.utils.safestring import mark_safe

from langacore.kit.django.helpers import render

from spiralear.website.models import Page, Url, Content, Block
from spiralear.website.models import Language as Lang

EN = Lang.en.id
PL = Lang.pl.id

_lang_mapping = {
        'en': EN,
        'pl': PL,
}


def _generate_menu(lang, lang_symbol, parent=None):
    menu = []
    for page in Page.objects.filter(parent=parent).order_by("index"):
        try:
            url = Url.objects.get(page=page, lang=lang)
            content = Content.objects.get(url=url)

            # ugly hack
            if url.url:
                title = content.title.upper()
            else:
                title = "SPIRAL EAR"

            children = _generate_menu(lang, lang_symbol, page)
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
    def __init__(self, request):
        self.request = request
        self.blocks = {}

    def add(self, block):
        text = "{%load validation%}\n" + block.text
        self.blocks[block.name] = Template(text)

    def __getitem__(self, key):
        r = self.request
        get = defaultdict(lambda: '')
        # cannot use dict.update() because request.GET is really
        # a multi-dict
        for k in r.GET:
            get[k] = r.GET[k]
        return mark_safe(self.blocks[key].render(RequestContext(r,
                                                 {'get': get})))


def handler(request, url, lang):
    url = url.lower()
    lang_symbol = lang.lower()
    lang = _get_lang(lang)
    try:
        u = Url.objects.get(url=url, lang=lang)
        c = Content.objects.get(url=u)
    except (Url.DoesNotExist, Content.DoesNotExist):
        redirect(request)

    menu = _generate_menu(lang, lang_symbol)
    _mark_active(menu, u)
    try:
        other = u.page.get_others(lang)[0]
        alternative_lang_url = other.full_link()
        alternative_lang_desc = other.lang_description(long=True)
    except Url.DoesNotExist:
        pass

    banner = randint(1, 3)
    c.block = BlockRenderer(request)
    for b in Block.objects.filter(content=c):
        c.block.add(b)

    return render(request, c.template, locals())


def _get_lang(language):
    if language in _lang_mapping:
        return _lang_mapping[language]
    else:
        return None


def _get_lang_symbol(language, alt=False):
    if language == PL:
        return 'pl' if not alt else 'en'
    elif language == EN:
        return 'en' if not alt else 'pl'
    else:
        return ''


def redirect(request):
    return HttpResponseRedirect('/en/')
