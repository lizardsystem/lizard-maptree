import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s %(levelname)s %(message)s')

DEBUG = True
TEMPLATE_DEBUG = True
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db'},
    }
SITE_ID = 1
INSTALLED_APPS = [
    'lizard_maptree',
    'lizard_map',
    'lizard_ui',
    'lizard_security',
    'south',
    'django.contrib.staticfiles',
    'compressor',
    'django_nose',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    ]
ROOT_URLCONF = 'lizard_maptree.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

# Used for django.contrib.staticfiles
STATIC_URL = '/static_media/'
MEDIA_URL = '/'
MEDIA_ROOT = 'media'
STATICFILES_FINDERS = (
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )
COMPRESS_ROOT = 'media'
COMPRESS_ENABLED = False
TEMPLATE_CONTEXT_PROCESSORS = (
    # Default items.
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    # Needs to be added for django-staticfiles to allow you to use
    # {{ STATIC_URL }}myapp/my.css in your templates.
    'staticfiles.context_processors.static_url',
    )

LIZARD_MAPTREE_STANDALONE = True

SECRET_KEY = "Does not need to be secret"

try:
    # Import local settings that aren't stored in svn.
    from lizard_maptree.local_testsettings import *
except ImportError:
    pass
