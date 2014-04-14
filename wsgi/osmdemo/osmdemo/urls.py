from django.conf.urls import patterns, include, url
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

static_dir = os.path.join(os.path.join(os.getcwd(),'osmdemo'),'static')
print static_dir

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

	url(r'^', include('questionnaire.urls',namespace='questionnaire')),
)

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()
