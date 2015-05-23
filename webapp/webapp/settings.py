"""
Django settings for webapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ek_ftj5+=z+k6e*lh$1!o20a0(76_5rrb@rj=ldggu(n5h1zq$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
 #   'debug_toolbar',
    'smartClass',
    'testserver',
#    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

WSGI_APPLICATION = 'webapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartclass',
        'USER': 'smartclass',
        'PASSWORD': 'smartclass',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS':{
            'init_command':"SET foreign_key_checks = 0;",
        },
        'STORAGE_ENGINE': 'INNODB ',
    }
}
TEMPLATE_DIRS = (
   os.path.join(BASE_DIR,'/smartClass/templates'),
#   '/home/chy/work/git/smartclass/webapp/smartClass/templates',
)
AUTH_USER_MODEL='smartClass.MyUser'
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',

    'debug_toolbar.panels.timer.TimerDebugPanel',

    #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',

    'debug_toolbar.panels.headers.HeaderDebugPanel',

    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',

    'debug_toolbar.panels.template.TemplateDebugPanel',

    'debug_toolbar.panels.sql.SQLDebugPanel',

    'debug_toolbar.panels.signals.SignalDebugPanel',

#    'debug_toolbar.panels.logger.LoggingPanel',
)
INTERAL_IPS = ('127.0.0.1',)
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),)
STATIC_URL = '/static/'
LOGIN_URL="/smartClass/teacher/login/"

#session expire time ,30 minutes
SESSION_COOKIE_AGE = 60*30
