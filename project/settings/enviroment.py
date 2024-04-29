from pathlib import Path
from utils.enviroment import *
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE') # noqa E501

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: list[str] = parse_coma_separated_str_to_list(get_env_variable('ALLOWED_HOSTS')) # noqa E501
CSRF_TRUSTED_ORIGINS: list[str] = parse_coma_separated_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS')) # noqa E501

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'