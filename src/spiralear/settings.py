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

from langacore.kit.django import current_dir_support
execfile(current_dir_support)

from langacore.kit.django import namespace_package_support
execfile(namespace_package_support)

#
# common stuff for each install
#

ADMINS = ((u'Łukasz Langa', 'lukasz@langa.pl'),)
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl-pl'
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = CURRENT_DIR + 'media'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'spiralear.urls'
TEMPLATE_DIRS = (
    CURRENT_DIR + 'templates/',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'langacore.kit.django.common',
    'spiralear.website',
)

#
# stuff that should be customized in settings_local.py
#

SECRET_KEY = '-^kuq@#gnr9u8=@v7m=q98apqo2w&j87*gz0h(t#xut_&6spgl'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': CURRENT_DIR + 'development.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

from langacore.kit.django import profile_support
execfile(profile_support)
