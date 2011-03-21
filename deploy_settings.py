from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
INSTALLED_APP += (
    'gunicorn',
)
