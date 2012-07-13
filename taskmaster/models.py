#!/usr/bin/env python
# encoding: utf-8
"""
models.py - data modells for AppEngine/ndb

Created by Maximillian Dornseif on 2009-11-15.
Copyright (c) 2009, 2012 Maximillian Dornseif. All rights reserved.
"""

import random
import time
import hashlib
import base64

from google.appengine.ext import ndb  


class Account(ndb.Model):
    """Represents a Twitter Account"""
    twitter_user = ndb.StringProperty(default='')
    verified_twitter_user = ndb.StringProperty(default='')
    email = ndb.StringProperty(default='')
    public_name = ndb.StringProperty(default='')
    private_name = ndb.StringProperty(default='')

    def __unicode__(self):
        if self.public_name:
            return u'%s' % self.public_name
        if self.email:
            return u'%s' % self.email


class Peep(ndb.Model):
    """Represents a person, company or location."""
    account = ndb.UserProperty()
    twitter_user = ndb.StringProperty(default='')
    email = ndb.StringProperty(default='')
    name = ndb.StringProperty(default='')
    private_name = ndb.StringProperty(default='')

    def __unicode__(self):
        if self.name:
            return u'%s' % self.name
        if self.email:
            return u'%s' % self.email

    def get_url(self):
        return "/peeps/p%s/" % self.key.id()

    @property
    def designator(self):
        return 'p%s' % self.key.id()

STATE_CHOICES = (('new', 'new'), ('parsed', 'parsed'), ('done', 'done'), ('finished', 'finished'), ('deleted', 'deleted'))
TYP_CHOICES = (('do', 'do something'), ('provide', 'provide information'), ('upload', 'uplaod data'))

class Op(ndb.Model):
    """Op kodiert etwas, was zu tun ist.
    
       Example:
       Task: Please upload Information regarding the foobar
       Priority: Low|Medium|High
       From: md@hudora.de
       To: s.lau@hudora.de
       """
    account = ndb.UserProperty()
    peep = ndb.KeyProperty(kind=Peep)
    tweet_id = ndb.StringProperty(default='')
    task = ndb.TextProperty(default='')
    person = ndb.StringProperty(default='')
    typ = ndb.StringProperty(choices=[x[0] for x in TYP_CHOICES], default=TYP_CHOICES[0][0])
    state = ndb.StringProperty(choices=[x[0] for x in STATE_CHOICES], default=STATE_CHOICES[0][0])
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    def __unicode__(self):
        return (u'%s: %s' % (self.designator, self.task))[:40]

    def get_absolute_url(self):
        return "/ops/o%s/" % self.key.id()
    
    @property
    def designator(self):
        return 'o%s' % self.key.id()
