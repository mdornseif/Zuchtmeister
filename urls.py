# -*- coding: utf-8 -*-

"""URLs for testing taskmaster."""

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
# admin stuff
#(r'^admin/doc/', include('django.contrib.admindocs.urls')),
('^admin/', include(admin.site.urls)),

# ensure requests to favicon and robots.txt don't clutter logs
(r'favicon.ico', 'django.views.generic.simple.redirect_to', {'url': 'http://s.hdimg.net/layout06/favicon.png'}),
(r'robots.txt', 'django.views.generic.simple.redirect_to', {'url': 'http://s.hdimg.net/misc/robots.txt'}),

(r'^callback_googleappsauth/', 'googleappsauth.views.callback'),

url(r'^VvEf.NxhbheqqHtlhdgCQw--.html$', 'django.views.generic.simple.direct_to_template',
    {'template': 'taskmaster/welcome.html'}),
url(r'^$', 'django.views.generic.simple.direct_to_template',
    {'template': 'taskmaster/welcome.html'}),
url(r'^main/tasklist.opml$', 'taskmaster.views.opml_tasklist'),
url(r'^main/$', 'taskmaster.views.main_tasklist'),
url(r'^ops/(?P<designator>.+)/$', 'taskmaster.views.op_detail'),
url(r'^peeps/$', 'taskmaster.views.peep_list'),
url(r'^peeps/(?P<designator>.+)/$', 'taskmaster.views.peep_detail'),
url(r'^account/$', 'taskmaster.views.account_settings'),
url(r'^api/add_task', 'taskmaster.views.api_add_task'),
url(r'^api/delete_task', 'taskmaster.views.api_delete_task'),
url(r'^maintenance_every_minute', 'taskmaster.views.maintenance_pull_tweets'),

)

# when in development mode, serve static files 'by hand'
# in production the files should be placed at http://s.hdimg.net/taskmaster/
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './static'}),
    )
