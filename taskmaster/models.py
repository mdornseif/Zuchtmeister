#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Maximillian Dornseif on 2009-11-15.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import random
import time
from django.db import models
import hashlib
import base64

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_user = models.CharField(max_length=100, db_index=True, unique=True, default='', blank=True)
    verified_twitter_user = models.CharField(max_length=100, db_index=True, unique=True, default='', blank=True, editable=False)
    email = models.EmailField(max_length=100, db_index=True, unique=True)
    public_name = models.CharField(max_length=100, default='')
    private_name = models.CharField(max_length=100, default='', blank=True)

    def __unicode__(self):
        if self.public_name:
            return u'%s' % self.public_name
        if self.email:
            return u'%s' % self.email


class Peep(models.Model):
    """Represents a person, company or location."""
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, related_name='peeps')
    designator = models.CharField(max_length=250, default=None, null=True, blank=True, editable=False, db_index=True,
        unique=True)
    twitter_user = models.CharField(max_length=100, db_index=True, default='', blank=True)
    email = models.EmailField(max_length=100, db_index=True, default='', blank=True)
    name = models.CharField(max_length=100, default='', db_index=True)
    private_name = models.CharField(max_length=100, default='', blank=True)

    def __unicode__(self):
        if self.name:
            return u'%s' % self.name
        if self.email:
            return u'%s' % self.email

    def get_absolute_url(self):
        return "/peeps/%s/" % self.designator


def _peep_post_save_cb(signal, sender, instance, **kwargs):
    """Erzeugt den Objektbezeichner nach dem ersten Speichern
    Vergleiche https://cybernetics.hudora.biz/intern/trac/wiki/NummernKreise."""
    if not instance.designator:
        chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), instance.id))
        instance.designator = "P%s" % base64.b32encode(chash.digest()).rstrip('=')[5:15]
        instance.save()
models.signals.post_save.connect(_peep_post_save_cb, Peep)


STATE_CHOICES = (('new', 'new'), ('parsed', 'parsed'), ('done', 'done'), ('finished', 'finished'), ('deleted', 'deleted'))
TYP_CHOICES = (('do', 'do something'), ('provide', 'provide information'), ('upload', 'uplaod data'))

class Op(models.Model):
    """Example:
       Task: Please upload Information regarding the foobar
       Priority: Low|Medium|High
       From: md@hudora.de
       To: s.lau@hudora.de
       """
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, related_name='ops')
    peep = models.ForeignKey(Peep, related_name='ops', blank=True, null=True)
    designator = models.CharField(max_length=250, default=None, null=True, blank=True, editable=False, db_index=True,
        unique=True)
    tweet_id = models.CharField(max_length=16, default=None, null=True, blank=True, editable=False, db_index=True,
        unique=True)
    task = models.TextField()
    person = models.EmailField(blank=True, default='')
    typ = models.CharField(max_length=32, choices=TYP_CHOICES, default=TYP_CHOICES[0][0])
    state = models.CharField(max_length=32, choices=STATE_CHOICES, default='new')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return (u'%s: %s' % (self.designator, self.task))[:40]

    def get_absolute_url(self):
        return "/ops/%s/" % self.designator


def _op_post_save_cb(signal, sender, instance, **kwargs):
    """Erzeugt den Objektbezeichner nach dem ersten Speichern
    Vergleiche https://cybernetics.hudora.biz/intern/trac/wiki/NummernKreise."""
    if not instance.designator:
        chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), instance.id))
        instance.designator = "S%s" % base64.b32encode(chash.digest()).rstrip('=')[5:15]
        instance.save()
models.signals.post_save.connect(_op_post_save_cb, Op)


#class TaskFulfillment(models.Model):
#    task = models.ForeignKey(Task, to_field='designator', related_name='fullfillment_set')
