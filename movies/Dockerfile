# Используем официальный базовый образ Python
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Предотвращаем создание .pyc файлов, экономим пространство
ENV PYTHONDONTWRITEBYTECODE=1
# Отключает буферизацию стандартного вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости Python и копируем только requirements.txt
# COPY requirements.txt /app/requirements.txt
COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

#EXPOSE 8000

# gunicorn
#CMD ["bash", "-c", "set -e && \
#    echo 'Collecting static files...' && python manage.py collectstatic --noinput && \
#    echo 'Applying migrations...' && python manage.py makemigrations && \
#    echo 'Running migrations...' && python manage.py migrate --noinput && \
#    if [ -f superuser.py ]; then echo 'Creating superuser...' && python manage.py shell < superuser.py; fi && \
#    echo 'Starting Gunicorn...' && gunicorn -c gunicorn.conf.py config.wsgi:application"]

# Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


CMD ["bash", "-c", "set -e && \
    echo 'Collecting static files...' && python manage.py collectstatic --noinput && \
    echo 'Applying migrations...' && python manage.py makemigrations && \
    echo 'Running migrations...' && python manage.py migrate --noinput && \
    if [ -f superuser.py ]; then echo 'Creating superuser...' && python manage.py shell < superuser.py; fi && \
    echo 'Starting...' && \
    if [ \"$MODE\" = 'gunicorn' ]; then gunicorn -c gunicorn.conf.py config.wsgi:application; else python manage.py runserver 0.0.0.0:\"$PORT\"; fi"]


#CMD ["sh", "-c", "if [ \"$MODE\" = 'gunicorn' ]; then gunicorn -c gunicorn.conf.py config.wsgi:application; else python manage.py runserver 0.0.0.0:8000; fi"]
