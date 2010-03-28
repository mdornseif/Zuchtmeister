#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by Maximillian Dornseif on 2010-03-28.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

from django.contrib import admin
from taskmaster.models import Account

admin.site.register(Account)