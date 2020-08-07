"""
Settings
-------------------------------
Django settings for TicketVise. Contains various settings for the project,
some custom.
"""
import os

from dotenv import load_dotenv

load_dotenv()

#: Project base directory.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET", "<SECRET_KEY_DEFAULT>")

#: Used to run Django in debug mode.
DEBUG = int(os.environ.get("DEBUG", True))

#: If ``True``, mails are sent when calling :func:`email.send_email`.
SEND_MAIL = int(os.environ.get("SEND_MAIL", False))

ALLOWED_HOSTS = ["*"]

#: Application definition
#: ~~~~~~~~~~~~~~~~~~~~~~

#: User model to use for authentication.
AUTH_USER_MODEL = "ticketvise.User"

#: Apps used for Django.
INSTALLED_APPS = [
    "ticketvise",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_celery_results",
]

#: Middleware used for Django.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
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
                "ticketvise.context_processors.global_context",
            ],
        },
    },
]

CSP_FRAME_ANCESTORS = ["https://uvadlo-tes.instructure.com", "https://*.uva.nl"]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
    "*.gstatic.com",
    "https://uicdn.toast.com/editor/latest/toastui-editor.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.min.css"
]
CSP_SCRIPT_SRC = [
    "'self'",
    "'unsafe-inline'",
    "*.gstatic.com",
    "'unsafe-eval'",
    "https://uicdn.toast.com/editor/latest/toastui-editor-all.min.js"
]
CSP_IMG_SRC = ["*", "data:"]
CSP_DEFAULT_SRC = ["'self'", "'unsafe-inline'", "'unsafe-eval'"]

CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = None
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
LTI_HOST = os.environ.get("LTI_HOST", "https://uva.ticketvise.com")
LTI_XML_CONFIG_URL = LTI_HOST + "/lti/config.xml"

#: Database to use.
DATABASES = {
    "default": {
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
DEFAULT_AVATAR_PATH = "/static/img/avatars/default-avatar.png"
#: Directory for uploaded avatar pictures.
AVATAR_DIRECTORY = "media/img/avatars"
#: Path to the default inbox image.
DEFAULT_INBOX_IMAGE_PATH = "/static/img/inboxes/default-inbox.png"
#: Directory for uploaded inbox images.
INBOX_IMAGE_DIRECTORY = "media/img/inboxes"
#: Set max upload size for files
FILE_UPLOAD_MAX_MEMORY_SIZE = 314572800

#: URLs for login and logout
#: ~~~~~~~~~~~~~~~~~~~

#: URL that users get redirected to on logout.
LOGOUT_REDIRECT_URL = "/"
#: Default URL that users get redirected to on login.
LOGIN_REDIRECT_URL = "/inboxes"
#: Default URL for the login page.
LOGIN_URL = "/login/"

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

#: URL path to the static folder.
STATIC_URL = "/static/"
#: File path to the static root.
STATIC_ROOT = os.path.join(BASE_DIR, "ticketvise/static")

#: Email settings
#: ~~~~~~~~~~~~~~~~~~~

#: Email host.
EMAIL_HOST = "smtp.zoho.com"
#: Email port to use.
EMAIL_PORT = 465
#: Email address to use.
EMAIL_HOST_USER = "noreply@ticketvise.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "noreply@ticketvise.com"

# Global settings:
#: These settings can be used when importing "from django.conf import settings".
GLOBAL_SETTINGS = {
    "email_address": EMAIL_HOST_USER,
}

#: Celery and Redis settings
#: ~~~~~~~~~~~~~~~~~~~~~~~~~

#: Broker URL.
CELERY_BROKER_URL = "redis://redis:6379"
#: Result backend.
CELERY_RESULT_BACKEND = "django-db"
#: Cache backend.
CELERY_CACHE_BACKEND = "django-cache"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

PAGE_SIZE = 25

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
        'level': 'WARNING',
    },
}

ROLE_GUEST_DISPLAY_NAME = os.getenv("ROLE_GUEST_DISPLAY_NAME", "Student")
ROLE_AGENT_DISPLAY_NAME = os.getenv("ROLE_AGENT_DISPLAY_NAME", "Teaching Assistant")
ROLE_MANAGER_DISPLAY_NAME = os.getenv("ROLE_MANAGER_DISPLAY_NAME", "Coordinator")