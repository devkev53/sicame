from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# LANGUAGES INTERNACIONALIZATION

LANGUAGES = [
    ('es', 'Español'),
    ('en', 'Englis')
]

LOCALE_PATHS = (
    (BASE_DIR / '../locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/ '../static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/ '../media'

# STATICFILES_DIRS = [
#   BASE_DIR/ '../build/static/'
# ]

# CHANGE AUTH_USER_MODEL

AUTH_USER_MODEL = 'registration.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'core.backend.AuthEmailBackend',
]