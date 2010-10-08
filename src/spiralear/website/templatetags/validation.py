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

register = template.Library()

@register.filter
def check(value, arg):
    """Usage: {{string|check:"/regex/default"}}
    
    If the string doesn't match the regex, switches to the default."""

    _, regex, default = arg.split(arg[0], 2)
    if value and re.match(regex, value):
        default = value 
    return default

@register.filter
def strip(value):
    return unicode(value).strip()
