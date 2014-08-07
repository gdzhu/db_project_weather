from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

# from MyBlog.views import *

urlpatterns = patterns(
    '',
    
    # project urls
    url(r'^', include('project.urls')),

    # allauth urls
    url(r'^accounts/', include('allauth.urls')),
    
    # admin
    url(r'^admin/', include(admin.site.urls)),
)
