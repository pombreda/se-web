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
def GET(value, arg):
    """Usage: {{string|get:"block variable regex default"}}
    
    Fills encountered {{variable}} instances in the given string
    with GET arguments as long as they match the given regular
    expression."""

    block, variable, regex, default = arg.split(" ", 3)
    if variable in value.request.GET:
        var = value.request.GET[variable]
        if re.match(regex, var):
            default = var
    return mark_safe(value[block].replace("{{" + variable + "}}", default))
