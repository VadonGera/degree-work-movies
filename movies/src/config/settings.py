"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import yaml
import logging.config

load_dotenv()  # Загружаем базовые переменные из файла .env

# # Определяем текущую среду, по умолчанию 'development'
# current_env = str(os.getenv("DJANGO_ENV", "development"))
# env_file = f".env.{current_env}"  # Определяем путь к нужному .env файлу
# load_dotenv(env_file)  # Дозагружаем переменные из файла


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY", "default_secret_key"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = str(os.getenv("ALLOWED_HOSTS", "127.0.0.1")).split(",")

# ======= Логирование ===========================

# Отключаем автонастройку логирования
LOGGING_CONFIG = None
# Путь к файлу logging.yaml
LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, "logging.yaml")
# Загрузка конфигурации логирования
try:
    with open(LOGGING_CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)
        print("Конфигурация логирования успешно загружена.")
except Exception as e:
    print(f"Ошибка загрузки конфигурации логирования: {e}")

# ===============================================


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS += [
    "rest_framework",
    "movies",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # указываем путь к каталогу с шаблонами
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": str(os.getenv("PGSQL_ENGINE")),
        "NAME": str(os.getenv("PGSQL_DB")),
        "USER": str(os.getenv("PGSQL_USER")),
        "PASSWORD": str(os.getenv("PGSQL_PASSWORD")),
        "HOST": str(os.getenv("PGSQL_HOST", "127.0.0.1")),
        "PORT": str(os.getenv("PGSQL_PORT")),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGES = [
    ("en", "English"),
    ("ru", "Russian"),
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# куда перенаправлять пользователя после успешной авторизации.
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
