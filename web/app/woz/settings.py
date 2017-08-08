# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_secret = "default-secret"
SECRET_KEY = os.getenv("SECRET_KEY", default_secret)

DEBUG = SECRET_KEY == default_secret

ALLOWED_HOSTS = ['*']

DATAPUNT_API_URL = os.getenv(
    # note the ending /
    'DATAPUNT_API_URL', 'https://api.data.amsterdam.nl/')

# Application definition

INSTALLED_APPS = (
    'health',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_extensions',

    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_swagger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'woz.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'woz'),
        'USER': os.getenv('DB_USER', 'woz'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': os.getenv('DATABASE_PORT_5432_TCP_ADDR', 'database'),
        'PORT': os.getenv('DATABASE_PORT_5432_TCP_PORT', '5432'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

ROOT_URLCONF = 'woz.urls'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

INTERNAL_IPS = ['127.0.0.1']

REST_FRAMEWORK = dict(
    PAGE_SIZE=25,
    MAX_PAGINATE_BY=100,

    DEFAULT_PAGINATION_CLASS='drf_hal_json.pagination.HalPageNumberPagination',
    DEFAULT_PARSER_CLASSES=('drf_hal_json.parsers.JsonHalParser',),

    DEFAULT_AUTHENTICATION_CLASSES=(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    COERCE_DECIMAL_TO_STRING=False,
)

CORS_ORIGIN_ALLOW_ALL = True  # if True, the whitelist will not be used and all origins will be accepted

CORS_ORIGIN_REGEX_WHITELIST = (
    '^(https?://)?localhost(:\d+)?$',
    '^(https?://)?.*\.datapunt.amsterdam\.nl$',
    '^(https?://)?.*\.amsterdam\.nl$',
)

# Security

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# Generate https links
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
