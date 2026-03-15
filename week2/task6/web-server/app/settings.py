SECRET_KEY = 'simple-secret-key-for-dev'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

MIDDLEWARE = []

ROOT_URLCONF = 'app.urls'

DATABASES = {}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
