# Django settings for website project.

import os
import sys
from os.path import dirname


PROJECT_PATH = dirname(dirname(dirname(os.path.realpath(__file__))))
TEMPLATE_PATH = PROJECT_PATH + '/user_raw'
APP_PATH = dirname(os.path.realpath(__file__))

sys.path.insert(0, PROJECT_PATH)

# print >> sys.stderr, TEMPLATE_PATH
# print >> sys.stderr, APP_PATH

# 4store
FOURSTORE_KBNAME = "linkedin"
FOURSTORE_PORT = 6742
SPARQL_ENDPOINT = "http://localhost:6667/sparql/"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

## Global constants
NUM_FILES = 10
NUM_GROUPS = 5

# print APP_PATH + "/db/website.db"

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': APP_PATH + "/db/survey.db",					  # Or path to database file if using sqlite3.
		# The following settings are not used with sqlite3:
		'USER': '',
		'PASSWORD': '',
		'HOST': '',					  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
		'PORT': '',					  # Set to empty string for default.
	}
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/survey/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	'django.contrib.staticfiles.finders.DefaultStorageFinder',
	'less.finders.LessFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@v2@tp@20p54qq5-opfa%#_+od^y$#_^lyw9%4wk_9l=0_nq83'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	# 'django.contrib.messages.middleware.MessageMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_DIRS = (
	TEMPLATE_PATH,
	APP_PATH + '/html',
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.

)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'twitter_bootstrap',
	'less',
	'pipeline',
	'survey',
	'gunicorn',
	'django_evolution',
	'fourstore',
	# Uncomment the next line to enable the admin:
	# 'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
	'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
	'bootstrap': {
		'source_filenames': (
			'less/bootstrap.less',
			'less/responsive.less'
		),
		'output_filename': 'css/b.css',
		'extra_context': {
		'media': 'screen,projection',
		},
	},
}

PIPELINE_JS = {
	'bootstrap': {
		'source_filenames': (
			'js/bootstrap-transition.js',
			'js/bootstrap-alert.js',
			'js/bootstrap-modal.js',
			'js/bootstrap-dropdown.js',
			'js/bootstrap-scrollspy.js',
			'js/bootstrap-tab.js',
			'js/bootstrap-tooltip.js',
			'js/bootstrap-popover.js',
			'js/bootstrap-button.js',
			'js/bootstrap-collapse.js',
			'js/bootstrap-carousel.js',
			'js/bootstrap-typeahead.js',
			'js/bootstrap-affix.js',
		),
		'output_filename': 'js/b.js',
	},
}
