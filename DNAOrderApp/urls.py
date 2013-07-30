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
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^order/', include('DNAOrderApp.order.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Django does not serve MEDIA_ROOT by default, that would be dangerous in production
# environment. But in development stage, we could cut short. Pay attention to the 
# last line. That line enables Django to serve files from MEDIA_URL. This works only in developement stage.

# From django-jquery-file-upload

import os
urlpatterns += patterns('',
	url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)
