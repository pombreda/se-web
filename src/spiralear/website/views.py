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

from django.http import HttpResponseRedirect

from langacore.kit.django.helpers import render

from spiralear.website.models import Page, Block, Language

PL = Language.pl.id
EN = Language.en.id

_menu = (
    {
        PL: ['glowna/', 'Strona główna'],
        EN: ['frontpage/', 'Spiral Ear'],
        'img': 'home',
    },
    {
        PL: ['produkty/', 'Produkty'],
        EN: ['products/', 'Products'],
        'img': 'prod',
    },
    {
        PL: ['galeria/', 'Galeria'],
        EN: ['gallery/', 'Gallery'],
        'img': 'gal',
    },
    {
        PL: ['zamowienia/', 'Zamówienia'],
        EN: ['ordering/', 'Ordering'],
        'img': 'ord',
    },
    {
        PL: ['kontakt/', 'Kontakt'],
        EN: ['contact/', 'Contact'],
        'img': 'contact',
    }
)

def handler(request, page, lang):
    try:
        p = Page.objects.get(url=page, lang=lang)
    except Page.DoesNotExist:
        #redirect(request)
        p = Page(url=page, lang=lang, title=page, template=page + '.html')
        p.save()

    menu = []

    lang_symbol = 'pl' if lang == PL else 'en' if lang == EN else ''

    for entry in _menu:
        e = list(entry[lang])
        status = 'inactive'
        if e[0] == page + '/':
            status = 'active'
        if entry['img'] == 'home':
            e[0] = ''
        menu.append(('/{}/{}'.format(lang_symbol,
                        e[0]),
                    e[1],
                    '/media/img/menu/{}_{}_{}.png'.format(
                        lang_symbol,
                        entry['img'],
                        status)))

    return render(request, p.template, locals())

def redirect(request):
    return HttpResponseRedirect('/en/')
