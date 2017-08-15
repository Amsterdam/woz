import os

from woz.settings_common import * # noqa F403
from woz.settings_common import INSTALLED_APPS, DEBUG
from woz.settings_databases import Location_key, \
    get_docker_host, \
    get_database_key, \
    OVERRIDE_HOST_ENV_VAR, \
    OVERRIDE_PORT_ENV_VAR

INSTALLED_APPS += [
    'woz.health',
    'woz.wozdata',
]

ROOT_URLCONF = 'woz.urls'

WSGI_APPLICATION = 'woz.wsgi.application'

DATABASE_OPTIONS = {
    Location_key.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'woz'),
        'USER': os.getenv('DATABASE_USER', 'woz'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    Location_key.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'woz'),
        'USER': os.getenv('DATABASE_USER', 'woz'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5459'
    },
    Location_key.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'woz'),
        'USER': os.getenv('DATABASE_USER', 'woz'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

# SWAGGER
SWAG_PATH = 'acc.api.data.amsterdam.nl/woz/docs'

if DEBUG:
    SWAG_PATH = '127.0.0.1:8000/woz/docs'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
    'api_path': '/',

    'enabled_methods': [
        'get',
    ],

    'api_key': '',
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,

    'is_authenticated': False,
    'is_superuser': False,

    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,

    'protocol': 'https' if not DEBUG else '',
    'base_path': SWAG_PATH,

    'info': {
        'contact': 'atlas.basisinformatie@amsterdam.nl',
        'description': 'This is the woz API server.',
        'license': 'Not known yet',
        'termsOfServiceUrl': 'https://atlas.amsterdam.nl/terms/',
        'title': 'Tellus',
    },

    'doc_expansion': 'list',
}

# HEALTH_MODEL = 'dataset.Woz'

LOCAL_DATA_DIR = os.getenv('LOCAL_DATA_DIR', '/app/data')
OBJECTSTORE_PASSWORD = os.getenv('BAG_OBJECTSTORE_PASSWORD', 'insecure')
OBJECTSTORE_TENNANT = os.getenv('BAG_OBJECTSTORE_TENNANT_NAME', 'BGE000081_BAG')
OBJECTSTORE_TENNANT_ID =  os.getenv('BAG_OBJECTSTORE_TENNANT_ID', '4f2f4b6342444c84b3580584587cfd18')

DATAPUNT_AUTHZ = {
    'JWT_SECRET_KEY': os.getenv('JWT_SHARED_SECRET_KEY', 'insecureeeeeeeeeeeeeeeeeeeeeeeeeee'),
    'JWT_ALGORITHM': "HS256"
}
