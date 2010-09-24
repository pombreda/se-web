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

from random import randint

from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from langacore.kit.django.helpers import render

from spiralear.website.models import Page, Block, Language

PL = Language.pl.id
EN = Language.en.id

_menu = (
    {
        PL: ['glowna/', 'STRONA GŁÓWNA'],
        EN: ['frontpage/', 'SPIRAL EAR'],
        'home': True,
    },
    {
        PL: ['produkty/', 'PRODUKTY'],
        EN: ['products/', 'PRODUCTS'],
    },
    {
        PL: ['galeria/', 'GALERIA'],
        EN: ['gallery/', 'GALLERY'],
    },
    {
        PL: ['zamowienia/', 'ZAMÓWIENIA'],
        EN: ['ordering/', 'ORDERING'],
    },
    {
        PL: ['kontakt/', 'KONTAKT'],
        EN: ['contact/', 'CONTACT'],
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
        status = ''
        if e[0] == page + '/':
            status = mark_safe('class="active"')
        if 'home' in entry:
            e[0] = ''
        menu.append(('/{}/{}'.format(lang_symbol,
                        e[0]),
                    status,
                    e[1]))

    banner = randint(1, 3)

    return render(request, p.template, locals())

def redirect(request):
    return HttpResponseRedirect('/en/')
