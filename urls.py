from django.conf.urls.defaults import include
from django.contrib import admin

from dselector import Parser

admin.autodiscover()
parser = Parser()
url = parser.url


urlpatterns = parser.patterns('',
    # url(r'!', include('century.tracker.urls')),

    url(r'admin/doc/!', include('django.contrib.admindocs.urls')),
    url(r'admin/!', include(admin.site.urls)),
)
