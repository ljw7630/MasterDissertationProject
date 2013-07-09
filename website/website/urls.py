from django.conf.urls import patterns, include, url
import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^hello/$', views.hello),
	('^time/$', views.current_datetime),
	(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
	('^$', views.hello),
	('^consent/$', views.consent),
	('^print_users/$', 'survey.views.print_users'),
	('^print_form/$', 'survey.views.print_form'),
	('^finish/$', 'survey.views.finish'),
	# Examples:
	# url(r'^$', 'website.views.home', name='home'),
	# url(r'^website/', include('website.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)
