from django.conf.urls.defaults import *
from django.conf import settings
from auth.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'^home/$', home),
    (r'^info/?$', info),
    (r'^login/twitter/?$', login_with_twitter),
    (r'^login/facebook/?$', login_with_facebook),
    (r'^login/callback/?$', callback),
    (r'^logout/?$', logout),
    (r'^about/$', about),
    (r'^admin/', include(admin.site.urls)),
    (r'^medios/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True
    }),
)
