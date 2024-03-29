import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qZDQQZ23EA.2AE2/EAEA.EA2E.AÈ23zDz;23::///23x212'

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'catalog.apps.CatalogConfig',
    'qrcodes.apps.QrcodesConfig',
    'achats.apps.AchatsConfig',
    'points.apps.PointsConfig',
    'rest_framework',
    'django_filters',
    'enigmes.apps.EnigmesConfig',
    'paris.apps.ParisConfig',
    'photos.apps.PhotosConfig',
    'repenigmes.apps.RepenigmesConfig',
    'events.apps.EventsConfig',
    'stockavatar.apps.StockavatarConfig',
    'histodefis.apps.HistodefisConfig',
    'pwa',
    'webpush',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas_ng.middleware.CASMiddleware'
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

ROOT_URLCONF = 'foodstockdjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


CAS_SERVER_URL = 'https://cas.dev.inpt.fr/'
CAS_VERSION = '3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
      #  'default': {
       #  'ENGINE': 'ENGINE',
      #    'NAME': 'NAME',
      #  'USER': 'USER',
      #   'PASSWORD': 'PASSWORD',
       #   'HOST': 'HOST',
      #    'PORT': 'PORT',
     # }
}


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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles/images')
MEDIA_URL = os.path.join(BASE_DIR, 'static/images/')


##PWA
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js/serviceworker.js')

PWA_APP_NAME = 'Jura7Park'
PWA_APP_DESCRIPTION = "Le site officiel de Jura7Park"
PWA_APP_THEME_COLOR = '#4fc3a1'
PWA_APP_BACKGROUND_COLOR = '#be4d25'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src': 'static/images/icon160.png',
		'sizes': '160x160'
	}
]
PWA_APP_ICONS_APPLE = [
	{
		'src': 'static/images/icon160.png',
		'sizes': '160x160'
	}
]
PWA_APP_SPLASH_SCREEN = [
	{
		'src': 'static/images/icon160.png',
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]

PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'fr-FR'


###NOTIFICATIONS
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BLo_y-eUa65rZAHRyCFWvNXKx_4FVY2jdFtsG0inusC-0-G3hqGXbpDmlEghElTLdWp4FLDmHOWd6G1N75kafp0",
    "VAPID_PRIVATE_KEY":"Myx7Pdho13OtwmV9zHD-utKjrUlb5HYmg2AmzsBcTuE",
    "VAPID_ADMIN_EMAIL": "asphalt8fr@gmail.com"
}