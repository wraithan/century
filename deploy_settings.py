from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
INSTALLED_APPS += (
    'gunicorn',
)
