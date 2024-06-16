"""
Settings
-------------------------------
Django settings for TicketVise. Contains various settings for the project,
some custom.
"""
import os

from msal.application import ConfidentialClientApplication

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

MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.environ.get("MICROSOFT_CLIENT_SECRET")
MICROSOFT_EMAIL_SCOPES = ["https://outlook.office.com/IMAP.AccessAsUser.All",
                          "https://outlook.office.com/POP.AccessAsUser.All", 
                          "https://outlook.office.com/SMTP.Send"]
MICROSOFT_AUTH = None
if MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET:
    MICROSOFT_AUTH = ConfidentialClientApplication(MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET)

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

CSP_FRAME_ANCESTORS = ["https://uvadlo-tes.instructure.com", "https://uvadlo-dev.test.instructure.com", "https://*.uva.nl"]
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
LTI_PUBLIC_KEY = os.environ.get("LTI_PUBLIC_KEY", """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwfiSy8Rx3Pw2y+7l1y5F
InGh5RUoELueVfCgmGo36DmqGspjWKsyaEu7GOki1Z6g8oaGtjRCHIacx8NqM4l4
LYRUuOA4NnTD2gAJDQBR0wG36/T8yD8bQy3Qkck4+h031nElicDfnHfWXV0Pp916
Ms0zyO3u7I/vwpJheR5wiwsthqMisEOSetqyOx4Y6lVg5KLc8zc5Gp/Wv/hIwwOj
CCPyTjZnwLjEkS7SMJhllYPJ7Kd9x48dhAic/cCwK49IUAKdVlGhyi3twn/xdYGB
Vfh8YTAbu2LFu3EBjJ3seco4Cv4oD1FX2FlxF9/mqiDgrllHFO30KiYoXnloi7St
h/zT9b2sbB3XRQ5UcZ982bvYffS22UjWJ/gnw40m1J5bVJrhBN+eUG64WSbw8mq5
EvgEOsb2Kgu50eZWzjEhQUD4b1NMYxMKXd6aRgjs7mS7x1q11M87T1FfAAyn07MR
Axbs4tfwAwb9xd0uCLfnFWlX9RiMygZMNRQttj8GZM6zkwKz4mdVgmWUS16snvog
qxWje0i2PWRvAwEZ7tFkbXngS04/Je9mW0iRT2Vbtzgcpb56luvWlCqd/GKDds4B
rGnRWAMWc8yulrbMEXYAbixlnqgYs/y+bbpKMz8K20Rl6GFba23IpkjMNUdGlOKL
APEBSOvPmjGsHoJChZ2gLOsCAwEAAQ==
-----END PUBLIC KEY-----""")
LTI_PRIVATE_KEY = os.environ.get("LTI_PRIVATE_KEY", """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----""")
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
        # "CONN_MAX_AGE": 600,
        # "CONN_HEALTH_CHECKS": True
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

#: URL paths for data
#: ~~~~~~~~~~~~~~~~~~~

#: Data url base.
DATA_URL = os.path.join(BASE_DIR, "ticketvise/data/")

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
AWS_S3_ENDPOINT_URL = ('https://' if AWS_S3_SECURE_URLS else 'http://') + os.environ.get("S3_ENDPOINT_URL", "s3:9000")
AWS_S3_CUSTOM_DOMAIN = f"{os.environ.get('S3_ENDPOINT_URL', 's3:9000')}/{AWS_STORAGE_BUCKET_NAME}"
AWS_DEFAULT_ACL = 'public-read'


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
    EMAIL_BACKEND = 'ticketvise.mail.send.OAuthCompatibleEmailBackend'
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
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}
