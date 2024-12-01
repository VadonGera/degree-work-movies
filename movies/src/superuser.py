import os
import django
from django.contrib.auth import get_user_model

# Настройка Django для доступа к моделям
django.setup()

User = get_user_model()

# Получение данных суперпользователя из переменных окружения
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

# Создание суперпользователя, если он не существует
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser <{username}> create")
else:
    print(f"Superuser <{username}> already exists")
