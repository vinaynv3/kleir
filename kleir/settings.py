"""
Django settings for kleir project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wwe&4m7#5p4zkt0bo1ov!@$@p$&u7jbmtamzf)@m%^pszp7(ma'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'PropertyDocs.apps.PropertydocsConfig',
    'user.apps.UserConfig',
    'ImageUpload.apps.ImageuploadConfig',
    'Technical.apps.TechnicalConfig',
    'Reports.apps.ReportsConfig',
    'Viewer.apps.ViewerConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'kleir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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



WSGI_APPLICATION = 'kleir.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if PROJECT_DIR == 'C:\Project\kleir\kleir':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            #'OPTIONS': {
            #    'read_default_file': 'C:\Program Files\MySQL\MySQL Server 8.0\kleir.cnf',
            #},
                'NAME': 'kleir',
                'USER': 'root',
                'PASSWORD': 'WinterMute531@',
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#forms template
CRISPY_TEMPLATE_PACK = 'bootstrap4'

#Login app variables
LOGIN_REDIRECT_URL = 'Home-Page'
LOGIN_URL = 'login'


"""
MEDIA - Images
"""
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'ImageUpload/media')

"""
HEROKU: Postgres database URL
"""
# Heroku: Update database configuration from $DATABASE_URL.
if os.getcwd() == '/app':
    import dj_database_url
    DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost')
    }
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

    # Honor the 'X-Forwarded-Proto' header for request.is_secure().
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']
    DEBUG = False
