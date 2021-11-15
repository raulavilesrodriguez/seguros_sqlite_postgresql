import dj_database_url
from decouple import config

DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='Casa1234')

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

if config('DJANGO_PRODUCTION', default=False, cast=bool):
    from .settings_production import *