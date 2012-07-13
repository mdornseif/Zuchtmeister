#!/usr/bin/env python
# encoding: utf-8
"""
taskmaster2.py - reimplementiert die Konzepte von Taskmaster

Created by Maximillian Dornseif on 2012-07-13.
Copyright (c) 2012 HUDORA. All rights reserved.
"""


import lib


from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import gaetk.handler


class Task(ndb.Model):
    """Task kodiert etwas, was zu tun ist.

       Example:
       Task: Please upload Information regarding the foobar
       From: md@hudora.de
       To: s.lau@hudora.de
       """
    account = ndb.UserProperty()
    summary = ndb.StringProperty()
    description = ndb.TextProperty()
    to = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    def __unicode__(self):
        return (u'%s: %s' % (self.designator, self.summary))[:40]

    def get_absolute_url(self):
        return "/tasks/o%s/" % self.key.id()

    @property
    def designator(self):
        return 'o%s' % self.key.id()


class TasklistHandler(gaetk.handler.BasicHandler):
    def get(self):
        user = users.get_current_user()
        tasks = Task.query().fetch(100)
        Task(account=user, summary='Software screiben', description='Unklar', to='m.dornseif@hudora.de').put()
        self.render(dict(title=u"Tasks",
                         tasks=tasks,
                         ), 'taskmaster2/main.html')

urls = [('^/tasks/$', TasklistHandler)]

app = ndb.toplevel(webapp.WSGIApplication(urls))


def main():
    util.run_wsgi_app(app)

if __name__ == '__main__':
    main()
