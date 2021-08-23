"""
Settings
-------------------------------
Django settings for TicketVise. Contains various settings for the project,
some custom.
"""
import os

#: Project base directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET", "<SECRET_KEY_DEFAULT>")

#: Used to run Django in debug mode.
DEBUG = int(os.environ.get("DEBUG", True))

#: If ``True``, mails are sent when calling :func:`email.send_email`.
SEND_MAIL = int(os.environ.get("SEND_MAIL", False))

DOMAIN = os.environ.get("DOMAIN", "localhost")
HOST = os.environ.get("HOST", DOMAIN)

ALLOWED_HOSTS = ["*"]

#: Application definition
#: ~~~~~~~~~~~~~~~~~~~~~~

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#: User model to use for authentication.
AUTH_USER_MODEL = "ticketvise.User"

#: Apps used for Django.
INSTALLED_APPS = [
    "ticketvise.config.TicketViseConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    'rest_framework.authtoken',
]

#: Middleware used for Django.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "csp.middleware.CSPMiddleware",
    "ticketvise.middleware.CurrentUserMiddleware",
]

#: URL configuration path.
ROOT_URLCONF = "ticketvise.urls"

#: Templates and context processors to use.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CSP_FRAME_ANCESTORS = ["https://uvadlo-tes.instructure.com", "https://*.uva.nl"]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'"]
CSP_SCRIPT_SRC = ["'self'", "'unsafe-inline'", "'unsafe-eval'"]
CSP_IMG_SRC = ["*", "data:"]
CSP_DEFAULT_SRC = ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://*.sentry.io"]

CSRF_COOKIE_SAMESITE = "" if DEBUG else "None"
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "" if DEBUG else "None"
SESSION_COOKIE_SECURE = not DEBUG

#: WSGI application path.
WSGI_APPLICATION = "ticketvise.wsgi.application"

#: Authentication backends for Django.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# PROXY
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#: LTI settings
#: ~~~~~~~~~~~~

LTI_KEY = os.environ.get("LTI_KEY", "<LTI_KEY_DEFAULT>")
LTI_SECRET = os.environ.get("LTI_SECRET", "<LTI_SECRET_DEFAULT>")
LTI_HOST = os.environ.get("LTI_HOST", "https://" + DOMAIN)
LTI_XML_CONFIG_URL = LTI_HOST + "/lti/config.xml"

#: Database to use.
DATABASES = {
    "default": {
        # postgres: django.db.backends.postgresql_psycopg2
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", 'ticketvise.sqlite3'),
        "USER": os.environ.get("SQL_USER", "ticketvise"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "Welkom01"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

#: URL paths for media
#: ~~~~~~~~~~~~~~~~~~~

#: Media url base.
MEDIA_URL = "/"
#: Media root path.
MEDIA_ROOT = os.path.join(BASE_DIR, "ticketvise/")
#: Path to the default user avatar image.
DEFAULT_AVATAR_PATH = "/img/default-avatar.png"
#: Directory for uploaded avatar pictures.
AVATAR_DIRECTORY = "media/img/avatars"
#: Path to the default inbox image.
DEFAULT_INBOX_IMAGE_PATH = "/img/default-inbox.png"
#: Directory for uploaded inbox images.
INBOX_IMAGE_DIRECTORY = "media/img/inboxes"

# S3 config
#: Set max upload size for files
AWS_S3_MAX_MEMORY_SIZE = 314572800
AWS_S3_FILE_OVERWRITE = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_SECURE_URLS = int(os.environ.get("S3_USE_HTTPS", True))
AWS_QUERYSTRING_AUTH = False

AWS_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY", "minio")
AWS_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_KEY", "Welkom01")

AWS_STORAGE_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "ticketvise")
AWS_S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "http://s3:9000")
AWS_S3_CUSTOM_DOMAIN = f"{HOST}/s3/{AWS_STORAGE_BUCKET_NAME}"


#: Password validation
#: ~~~~~~~~~~~~~~~~~~~

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

#: Internationalization
#: ~~~~~~~~~~~~~~~~~~~

#: Language used in the project.
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = False
USE_TZ = True

#: Time zone to use for the website.
TIME_ZONE = "Europe/Amsterdam"

#: Time format to use.
TIME_FORMAT = "H"
#: Datetime format to use.
DATETIME_FORMAT = "j N, Y, H:i"
#: Date format to use.
DATE_FORMAT = "j N, Y"

#: Static paths
#: ~~~~~~~~~~~~~~~~~~~
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

#: Email settings
#: ~~~~~~~~~~~~~~~~~~~
if SEND_MAIL:
    EMAIL_BACKEND = 'application.backend.ticketvise.mail.OAuthCompatibleEmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

EMAIL_HOST = os.getenv("SMTP_OUTBOUND_HOST", "smtp.sendgrid.net")
EMAIL_PORT = os.getenv("SMTP_OUTBOUND_PORT", 587)
EMAIL_HOST_USER = os.getenv("SMTP_OUTBOUND_USER", "apikey")
EMAIL_HOST_PASSWORD = os.getenv("SMTP_OUTBOUND_PASSWORD", "Welkom01")
EMAIL_USE_TLS = os.getenv("SMTP_TLS", True)
EMAIL_USE_SSL = os.getenv("SMTP_SSL", False)
DEFAULT_FROM_EMAIL = os.getenv("SMTP_OUTBOUND_FROM", "TicketVise <ticket@{}>".format(DOMAIN))
 
PAGE_SIZE = 25

ROLE_GUEST_DISPLAY_NAME = os.getenv("ROLE_GUEST_DISPLAY_NAME", "Student")
ROLE_AGENT_DISPLAY_NAME = os.getenv("ROLE_AGENT_DISPLAY_NAME", "Teaching Assistant")
ROLE_MANAGER_DISPLAY_NAME = os.getenv("ROLE_MANAGER_DISPLAY_NAME", "Coordinator")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

TOKEN_EXPIRED_AFTER_SECONDS = 86400

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ticketvise.security.token.ExpiringTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
