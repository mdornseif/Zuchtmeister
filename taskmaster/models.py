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

STATE_CHOICES = (('new', 'new'), ('finished', 'finished'), ('approved', 'approved'))
TYP_CHOICES = (('do', 'do something'), ('provide', 'provide information'), ('upload', 'uplaod data'))

class Task(models.Model):
    """Example:
       Task: Please upload Information regarding the foobar
       Priority: Low|Medium|High
       From: md@hudora.de
       To: s.lau@hudora.de
       """
    id = models.AutoField(primary_key=True)
    designator = models.CharField(max_length=250, default='', blank=True, editable=False, db_index=True,
        unique=True)
    description = models.TextField()
    source = models.EmailField()
    destination = models.EmailField()
    typ = models.CharField(max_length=32, choices=TYP_CHOICES, default=TYP_CHOICES[0][0])
    state = models.CharField(max_length=32, choices=STATE_CHOICES, default='new')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def _task_post_save_cb(signal, sender, instance, **kwargs):
    """Erzeugt den Objektbezeichner nach dem ersten Speichern
    Vergleiche https://cybernetics.hudora.biz/intern/trac/wiki/NummernKreise."""
    if not instance.designator:
        chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), instance.id))
        instance.designator = "TM%s" % base64.b32encode(chash.digest()).rstrip('=')
        instance.save()
models.signals.post_save.connect(_task_post_save_cb, Task)


class TaskFulfillment(models.Model):
    task = models.ForeignKey(Task, to_field='designator', related_name='fullfillment_set')
    