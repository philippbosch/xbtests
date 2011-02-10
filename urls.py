import os.path

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_ROOT, 'media')}),
    (r'^admin/', include(admin.site.urls)),
    url(r'^jssettings/$', 'django.views.generic.simple.direct_to_template', {'template': 'jssettings.js', 'mimetype': 'application/x-javascript', 'extra_context': {'settings':settings}}, name="jssettings"),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    
    (r'^', include('pagetests.urls')),
)
