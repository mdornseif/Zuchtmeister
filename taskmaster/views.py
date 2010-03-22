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

def api_add_task(request):
    destination = request.GET.get('person')
    description = request.GET.get('task')
    # source = request.user.email
    source = 'md@hudora.de'
    task = models.Task.objects.create(description=description, source=source, destination=destination)
    print task
    print task.id
    print task.designator
    return http.HttpResponse(task.designator)

class views(unittest.TestCase):
    def setUp(self):
        pass
    
if __name__ == '__main__':
    unittest.main()