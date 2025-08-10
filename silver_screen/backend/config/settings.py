import os
import socket
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG') 
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
LOCALE_PATHS = ['movies/locale']
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
LANGUAGE_CODE = 'ru-RU' 
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static" 
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ['172.20.0.1']

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': (
    #     "django_filters.rest_framework.DjangoFilterBackend",
    #     "rest_framework.filters.OrderingFilter"
    # ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10
    
# }
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}


# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
# }

# if DEBUG:    
# import socket
# hostname, _, ips =socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]


# hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# def show_toolbar(request):
#     return True
# SHOW_TOOLBAR_CALLBACK = show_toolbar

# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': False,
        }
    },
} 

include(
    'components/database.py',
) 
include(
    'components/installed_apps.py',
) 
include(
    'components/templates.py',
) 
include(
    'components/middleware.py',
) 
include(
    'components/auth_password_validators.py',
) 