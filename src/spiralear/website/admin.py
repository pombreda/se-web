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

from django.contrib import admin

from spiralear.website import models as m


class BlockInline(admin.TabularInline):
    model = m.Block
    max_num = 3


class PageAdmin(admin.ModelAdmin):
    search_fields = ("url", "title", "template")
    list_display = ("url", "lang", "title", "template")
    list_filter = ("lang",)
    inlines = [BlockInline]


admin.site.register(m.Page, PageAdmin)
