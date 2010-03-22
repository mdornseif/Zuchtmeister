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


def main_tasklist(request):
    tasks = models.Task.objects.all()
    return shortcuts.render_to_response('taskmaster/main.html', {'tasks': tasks})


def api_add_task(request):
    destination = request.GET.get('person')
    description = request.GET.get('task')
    # source = request.user.email
    source = 'md@hudora.de'
    task = models.Task.objects.create(description=description, source=source, destination=destination)
    return http.HttpResponse(task.designator)


class views(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()