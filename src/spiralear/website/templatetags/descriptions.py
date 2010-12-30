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

import re

from django import template
from django.utils.safestring import mark_safe

from spiralear.website.models import DescriptionGroup, Description, Language

register = template.Library()

@register.filter
def desc(value, arg):
    """Usage: {{string|desc:"lang/group"}}

    Provides a description value from the database using the specified
    language and group. If not available, returns an empty string."""

    lang, group = arg.split('/', 1)
    lang = Language.IDFromName(lang, fallback=Language.en.id)
    try:
        group = DescriptionGroup.objects.get(name=group)
        description = Description.objects.get(lang=lang, argument=value)
        result = description.value
    except (DescriptionGroup.DoesNotExist, Description.DoesNotExist):
        result = ""
    return result
