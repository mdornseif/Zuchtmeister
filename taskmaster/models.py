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


STATE_CHOICES = (('new', 'new'), ('finished', 'finished'), ('approved', 'approved'))
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
    
