# Copyright (c) 2013 Genome Research Ltd.
# 
# Author: Albertina Wong <aw18@sanger.ac.uk>
# 
# This file is part of DNAOrderApp.
# 
# DNAOrderApp is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# managing static files, css, images, https://docs.djangoproject.com/en/dev/howto/static-files/#django.conf.urls.static.static
from django.conf.urls.static import static
from django.conf import settings

# import autocomplete_light
# autocomplete_light.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DNAOrderApp.views.home', name='home'),
    # url(r'^DNAOrderApp/', include('DNAOrderApp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^/?admin/', include(admin.site.urls)),
    
    url(r'^/?order/', include('DNAOrderApp.order.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()

# Django does not serve MEDIA_ROOT by default, that would be dangerous in production
# environment. But in development stage, we could cut short. Pay attention to the 
# last line. That line enables Django to serve files from MEDIA_URL. This works only in developement stage.

# From django-jquery-file-upload

import os
urlpatterns += patterns('',
	url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)
