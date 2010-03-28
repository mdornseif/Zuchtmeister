#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by Maximillian Dornseif on 2009-11-15.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import unittest
from  taskmaster import models
from django import http
from django import shortcuts

from taskmaster import forms
import tweepy
from taskmaster import models
from taskmaster import twitter
from django.conf import settings


def main_tasklist(request):
    try:
        account = models.Account.objects.get(email=request.user.email)
    except models.Account.DoesNotExist:
        return http.HttpResponseRedirect('/account')
    tasks = account.ops.all()
    return shortcuts.render_to_response('taskmaster/main.html', {'tasks': tasks})


def account(request):
    try:
        instance = models.Account.objects.get(email=request.user.email)
    except models.Account.DoesNotExist:
        # create new account / empty form
        instance = None
        twitter_problem = False
    if request.method == 'POST':
        form = forms.AccountForm(request.POST, instance=instance)
        if form.is_valid():
            account = form.save()
            return http.HttpResponseRedirect('')
    else:
        if not instance:
            name = ' '.join([request.user.first_name, request.user.last_name]).strip()
            data = {'email': request.user.email, 'public_name': name, 'private_name': name}
            form = forms.AccountForm(data)
        else:
            if instance.twitter_user:
                twitter_problem = not twitter.connetion_ok(instance)
            form = forms.AccountForm(instance=instance)
    return shortcuts.render_to_response('taskmaster/account.html',
                                        {'form':form, 'twitter_problem': twitter_problem,
                                         'account': instance})


def maintenance_pull_tweets(request):
    twitter.handle_direct_messages()
    return http.HttpResponse('ok')


def api_add_task(request):
    taskid = request.GET.get('taskid')
    try:
        account = models.Account.objects.get(email=request.user.email)
    except models.Account.DoesNotExist:
        return http.HttpResponseRedirect('/account')
    person = request.GET.get('person')
    description = request.GET.get('task')
    # source = request.user.email
    task = models.Op.objects.create(account=account, task=description)
    return http.HttpResponse(task.designator)


def api_delete_task(request):
    taskid = request.GET.get('taskid')
    try:
        account = models.Account.objects.get(email=request.user.email)
    except models.Account.DoesNotExist:
        return http.HttpResponseRedirect('/account')
    task = account.ops.get(designator=taskid)
    task.delete()
    return http.HttpResponse('ok')

