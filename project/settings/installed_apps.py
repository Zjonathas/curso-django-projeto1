# Application definition

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # CORS headers
    'corsheaders',
    # Django rest framework
    'rest_framework',
    'rest_framework_simplejwt',
    # These are our apps
    'recipes',
    'authors',
    'tag',
]
