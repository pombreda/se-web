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

from datetime import datetime, timedelta

from django.db import models as db
from django.utils.safestring import mark_safe

from langacore.kit.django.helpers import Choices


class Language(Choices):
    _ = Choices.Choice

    en = _("English")
    pl = _("polski")


class Page(db.Model):
    index = db.PositiveIntegerField(verbose_name="indeks",
                                    help_text="do określenia kolejności")
    parent = db.ForeignKey("Page", verbose_name="rodzic", blank=True,
                           null=True)

    class Meta:
        verbose_name = "strona"
        verbose_name_plural = "strony"
        unique_together = ("index", "parent")
        ordering = ("index",) # Stupid, cannot use 'parent' because it causes
                              # "Infinite loop caused by ordering.". The
                              # hierarchy used is acyclical so I wonder...

    def __unicode__(self):
        c = self._get_content((Language.en.id, Language.pl.id))
        if not c:
            return "Strona bez treści"
        else:
            return "Strona '{}' ({})".format(c.title, c.url.get_lang_display())

    def get_others(self):
        return Url.objects.filter(page=self)

    def _get_content(self, langs):
        try:
            return Content.objects.get(url__lang=langs[0], url__page=self)
        except Content.DoesNotExist:
            langs = langs[1:]
            return self._get_content(langs) if langs else None


class Url(db.Model):
    page = db.ForeignKey(Page, verbose_name="strona")
    lang = db.PositiveIntegerField(verbose_name="język", choices=Language())
    url = db.CharField(verbose_name="URL", max_length=200, blank=True)

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Linki"
        unique_together = ("page", "lang")

    def __unicode__(self):
        return "Link /{} ({})".format(self.url, self.get_lang_display())

    def full_link(self):
        return "/{}/{}".format(self.lang_description(),
                               self.with_trailing_slash(if_nonempty=True))


    def with_trailing_slash(self, if_nonempty=False):
        if not if_nonempty or self.url:
            return self.url + "/"
        else:
            return self.url

    def lang_description(self, long=False):
        if self.lang == Language.en.id:
            return 'english' if long else 'en'
        elif self.lang == Language.pl.id:
            return 'polish' if long else 'pl'
        else:
            return ''

class Content(db.Model):
    url = db.ForeignKey(Url, verbose_name="URL", unique=True)
    title = db.CharField(verbose_name="tytuł", max_length=200)
    desc = db.TextField(verbose_name="Długi opis",
                        help_text="Do wyników w Google")
    template = db.CharField(verbose_name="Szablon", max_length=200)

    class Meta:
        verbose_name = "treść"
        verbose_name_plural = "treści"
        ordering = ("url__lang", "url__url", "title")

    def __unicode__(self):
        return "Treść strony '{}' ({})".format(self.title,
                                               self.url.get_lang_display())

class Block(db.Model):
    content = db.ForeignKey(Content, verbose_name="treść")
    name = db.CharField(verbose_name="nazwa bloku", max_length=200)
    text = db.TextField(verbose_name="tekst bloku")

    class Meta:
        verbose_name = "blok"
        verbose_name_plural = "bloki"

    def __unicode__(self):
        content = self.content
        return "Blok '{}' strony '{}' ({})".format(self.name,
                    content.title, content.url.get_lang_display())

def just_now():
    return datetime.now()

def next_month():
    return datetime.now() + timedelta(days=30)


class Newsfeed(db.Model):
    lang = db.PositiveIntegerField(verbose_name="język", choices=Language())
    date_from = db.DateTimeField(verbose_name="wyświetlane od",
            default=just_now)
    date_to = db.DateTimeField(verbose_name="wyświetlane do",
            default=next_month)
    content = db.TextField(verbose_name="treść")
    url = db.URLField(verbose_name="URL")

    class Meta:
        verbose_name = "newsfeed"
        verbose_name_plural = "wpisy newsfeed"
        ordering = ("date_from", "date_to", "content")

    def __unicode__(self):
        return "Newsfeed {} - {}".format(self.date_from, self.date_to)

    def save(self, *args, **kwargs):
        super(Newsfeed, self).save(*args, **kwargs)


class DescriptionGroup(db.Model):
    name = db.CharField(verbose_name="nazwa", max_length=200)

    class Meta:
        verbose_name = "grupa opisów"
        verbose_name_plural = "grupy opisów"

    def __unicode__(self):
        return self.name


class Description(db.Model):
    group = db.ForeignKey(DescriptionGroup, verbose_name="grupa")
    lang = db.PositiveIntegerField(verbose_name="język", choices=Language())
    argument = db.CharField(verbose_name="argument", max_length=200)
    value = db.TextField(verbose_name="wartość")

    class Meta:
        verbose_name = "opis"
        verbose_name_plural = "opisy"

    def __unicode__(self):
        return ("Opis z grupy '{}' dla argumentu '{}' w języku '{}'"
                "".format(self.group, self.argument, self.get_lang_display()))
