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

from django.db import models as db
from django.utils.safestring import mark_safe

from langacore.kit.django.helpers import Choices


class Language(Choices):
    _ = Choices.Choice

    en = _("English")
    pl = _("polski")


class BlockFinder(object):
    def __init__(self, page):
        self.page = page

    def __getattr__(self, name):
        try:
            block = Block.objects.get(page=self.page, name=name)
            return mark_safe(block.content)
        except Block.DoesNotExist:
            return ''


class Page(db.Model):
    url = db.CharField(verbose_name="URL", max_length=200)
    lang = db.PositiveIntegerField(verbose_name="język", choices=Language())
    title = db.CharField(verbose_name="tytuł", max_length=200)
    template = db.CharField(verbose_name="Szablon", max_length=200)

    class Meta:
        verbose_name = "strona"
        verbose_name_plural = "strony"

    def block(self):
        return BlockFinder(self)


class Block(db.Model):
    page = db.ForeignKey(Page, verbose_name="strona")
    name = db.CharField(verbose_name="nazwa bloku", max_length=200)
    content = db.TextField(verbose_name="treść")

    class Meta:
        verbose_name = "blok"
        verbose_name_plural = "bloki"
