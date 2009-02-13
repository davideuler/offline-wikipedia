from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wp_0_1/', include('wp_0_1.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    (r'^wiki/$','sample.page.views.first'),
    (r'^wiki/(?P<fname>.*)/$','sample.page.views.req_handler'),
    (r'^wiki/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'data/media'}),	
)
