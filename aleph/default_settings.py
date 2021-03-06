from celery.schedules import crontab
from tempfile import gettempdir
from os import environ as env, path

DEBUG = True
ASSETS_DEBUG = True
CACHE = True

APP_TITLE = 'Aleph'
APP_NAME = 'aleph'
APP_LOGO = '/static/images/aleph_small.png'
APP_FAVICON = '/static/images/aleph_small.png'
APP_BASEURL = 'http://localhost:5000/'

ARCHIVE_TYPE = 'file'
ARCHIVE_AWS_KEY_ID = env.get('AWS_ACCESS_KEY_ID')
ARCHIVE_AWS_SECRET = env.get('AWS_SECRET_ACCESS_KEY')
# ARCHIVE_BUCKET = 'aleph2-dev.pudo.org'
ARCHIVE_PATH = env.get('ARCHIVE_PATH', '/srv/data/aleph')


UPLOAD_FOLDER = path.join(gettempdir(), 'aleph_uploads')
MAX_CONTENT_LENGTH = 500 * 1024 * 1024

# Set up a custom SCSS file with additional style rules here.
CUSTOM_SCSS_PATH = None
CUSTOM_TEMPLATES_DIR = []

# Shown on the home page as a few sample queries:
SAMPLE_SEARCHES = ['Serbia', 'TeliaSonera', 'Vladimir Putin']

# Language configuration
DEFAULT_LANGUAGE = 'en'
LANGUAGES = ['en', 'fr', 'de', 'ru', 'es', 'nl', 'ro', 'ka',
             'ar', 'tr', 'lb', 'el', 'lt', 'uk', 'zh', 'be',
             'bg', 'bs', 'ja', 'cs', 'lv', 'pt', 'pl', 'hy',
             'hr', 'hi', 'he', 'uz', 'mo', 'mn', 'ur', 'sq',
             'ko', 'is', 'it', 'et', 'no', 'fa', 'sw', 'sl',
             'az']


TESSDATA_PREFIX = env.get('TESSDATA_PREFIX')
PDFTOPPM_BIN = env.get('PDFTOPPM_BIN', 'pdftoppm')
CONVERT_BIN = env.get('CONVERT_BIN', 'convert')
SOFFICE_BIN = env.get('SOFFICE_BIN', 'soffice')
WKHTMLTOPDF_BIN = env.get('WKHTMLTOPDF_BIN', 'wkhtmltopdf')
DDJVU_BIN = env.get('DDJVU_BIN', 'ddjvu')
MDB_TABLES_BIN = env.get('MDB_TABLES_BIN', 'mdb-tables')
MDB_EXPORT_BIN = env.get('MDB_EXPORT_BIN', 'mdb-export')
SEVENZ_BIN = env.get('SEVENZ_BIN', '7z')

SECRET_KEY = env.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL', 'sqlite:///aleph.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
ELASTICSEARCH_URL = env.get('BONSAI_URL', 'http://localhost:9200')

ALEMBIC_DIR = path.join(path.dirname(__file__), 'migrate')
ALEMBIC_DIR = path.abspath(ALEMBIC_DIR)

SPINDLE_URL = 'https://search.occrp.org/'
SPINDLE_API_KEY = None

CELERY_ALWAYS_EAGER = False
# CELERY_IGNORE_RESULT = True
# CELERYD_MAX_TASKS_PER_CHILD = 200
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
# CELERY_RESULT_PERSISTENT = False
# CELERY_ACKS_LATE = True
CELERY_BROKER_URL = env.get('RABBITMQ_BIGWIG_URL',
                            'amqp://guest:guest@localhost:5672//')
CELERY_IMPORTS = ('aleph.queue')

CELERYBEAT_SCHEDULE = {
    'alert-every-night': {
        'task': 'aleph.alerts.check_alerts',
        'schedule': crontab(hour=1, minute=30)
    },
    'reindex-entities': {
        'task': 'aleph.logic.entities.reindex_entities',
        'schedule': crontab(hour=1, minute=0, day_of_week=1)
    },
    'scheduled-crawlers': {
        'task': 'aleph.crawlers.execute_scheduled',
        'schedule': crontab(hour='*/6', minute=40)
    },
}

OAUTH = {
    'consumer_key': env.get('OAUTH_KEY'),
    'consumer_secret': env.get('OAUTH_SECRET'),
    'request_token_params': {
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    'base_url': 'https://www.googleapis.com/oauth2/v1/',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://accounts.google.com/o/oauth2/token',
    'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
}
