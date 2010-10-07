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


class UrlInline(admin.TabularInline):
    model = m.Url
    max_num = 3


class PageAdmin(admin.ModelAdmin):
    def get_name(self):
        return self.__unicode__()
    get_name.short_description = "Strona"

    list_display = (get_name,)
    ordering = ("parent", "index")
    inlines = [UrlInline]

admin.site.register(m.Page, PageAdmin)


class BlockInline(admin.TabularInline):
    model = m.Block
    max_num = 3


class ContentAdmin(admin.ModelAdmin):
    def url_lang(self):
        return self.url.get_lang_display()
    url_lang.short_description = "Język"

    def url_url(self):
        return "/" + self.url.url
    url_url.short_description = "URL"

    search_fields = ("url__url", "title", "template")
    list_display = ("title", url_lang, url_url, "template")
    inlines = [BlockInline]


admin.site.register(m.Content, ContentAdmin)
