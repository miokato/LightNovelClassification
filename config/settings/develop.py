from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_LN_CLASSIFICATION')

DEBUG = True

ALLOWED_HOSTS = []
