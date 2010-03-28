#!/usr/bin/env python
# encoding: utf-8
"""
forms.py

Created by Maximillian Dornseif on 2010-03-28.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

from django.forms import ModelForm
from taskmaster import models

# Create the form class.
class AccountForm(ModelForm):
     class Meta:
         model = models.Account
